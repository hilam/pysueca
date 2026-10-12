"""Testes do servidor — assentos, intenções e broadcast (sprint 05)."""

import asyncio
from contextlib import asynccontextmanager

from pysueca.carta import Carta
from pysueca.protocolo import (
    Entrar,
    Erro,
    Estado,
    Jogar,
    Mensagem,
    Responder,
    desserializar,
    serializar,
)
from pysueca.servidor import Servidor

TIMEOUT = 1.0


@asynccontextmanager
async def mesa():
    """O servidor escutando em `127.0.0.1` na porta efêmera, fechado ao final."""
    servidor = Servidor()
    tcp = await servidor.iniciar("127.0.0.1", 0)
    try:
        porta = tcp.sockets[0].getsockname()[1]
        yield servidor, porta
    finally:
        tcp.close()


async def enviar(escritor: asyncio.StreamWriter, mensagem: Mensagem) -> None:
    """Manda a mensagem e espera o fio aceitar."""
    escritor.write(serializar(mensagem))
    await escritor.drain()


async def receber(leitor: asyncio.StreamReader) -> Mensagem:
    """A próxima mensagem da conexão, com timeout curto."""
    linha = await asyncio.wait_for(leitor.readline(), TIMEOUT)
    return desserializar(linha)


async def sentar(porta: int, nome: str) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    """Uma conexão de cliente que já mandou `entrar`."""
    leitor, escritor = await asyncio.open_connection("127.0.0.1", porta)
    await enviar(escritor, Entrar(nome))
    return leitor, escritor


async def fechar(*conexoes: tuple[asyncio.StreamReader, asyncio.StreamWriter]) -> None:
    """Fecha as conexões de cliente e espera o fio aceitar."""
    for _, escritor in conexoes:
        escritor.close()
        await escritor.wait_closed()


async def drenar(leitor: asyncio.StreamReader) -> Estado:
    """O último snapshot da conexão, descartando os broadcasts anteriores."""
    ultimo: Estado | None = None
    while True:
        try:
            linha = await asyncio.wait_for(leitor.readline(), 0.05)
        except TimeoutError:
            break
        if not linha:
            break
        mensagem = desserializar(linha)
        if isinstance(mensagem, Estado):
            ultimo = mensagem
    assert ultimo is not None
    return ultimo


async def nada(leitor: asyncio.StreamReader) -> None:
    """Assere que a conexão não recebeu nada no timeout curto."""
    try:
        linha = await asyncio.wait_for(leitor.read(1), 0.05)
    except TimeoutError:
        return
    raise AssertionError(f"mensagem inesperada: {linha!r}")


async def sentar_quatro(porta: int) -> list[tuple[asyncio.StreamReader, asyncio.StreamWriter]]:
    """Quatro conexões sentadas nos quatro assentos, cada uma já com o snapshot."""
    conexoes = [await sentar(porta, nome) for nome in ("Ana", "Bia", "Caio", "Duda")]
    for leitor, _ in conexoes:
        await receber(leitor)
    return conexoes


async def mesa_pronta(
    porta: int,
) -> tuple[list[tuple[asyncio.StreamReader, asyncio.StreamWriter]], list[Estado]]:
    """Quatro assentos sentados e a mão preparada, com o snapshot de cada um."""
    conexoes = await sentar_quatro(porta)
    respondente = (await drenar(conexoes[0][0])).respondente
    assert respondente is not None
    await enviar(conexoes[respondente][1], Responder(True))
    snapshots = [await drenar(leitor) for leitor, _ in conexoes]
    return conexoes, snapshots


def test_entrar_senta_no_primeiro_assento_livre() -> None:
    async def cenario() -> None:
        async with mesa() as (_, porta):
            leitor, escritor = await sentar(porta, "Ana")

            snapshot = await receber(leitor)

            assert isinstance(snapshot, Estado)
            assert snapshot.assentos == ["Ana", None, None, None]
            assert snapshot.mao == []
            assert snapshot.contagens == [0, 0, 0, 0]
            await fechar((leitor, escritor))

    asyncio.run(cenario())


def test_nome_ja_sentado_e_ativo_e_recusado() -> None:
    async def cenario() -> None:
        async with mesa() as (servidor, porta):
            conexoes = await sentar_quatro(porta)

            leitor, escritor = await asyncio.open_connection("127.0.0.1", porta)
            await enviar(escritor, Entrar("Ana"))
            resposta = await receber(leitor)

            assert resposta == Erro("nome_em_uso")
            assert servidor.nomes == ["Ana", "Bia", "Caio", "Duda"]
            await fechar((leitor, escritor), *conexoes)

    asyncio.run(cenario())


def test_mesa_cheia_recusa_o_quinto() -> None:
    async def cenario() -> None:
        async with mesa() as (servidor, porta):
            conexoes = await sentar_quatro(porta)

            leitor, escritor = await asyncio.open_connection("127.0.0.1", porta)
            await enviar(escritor, Entrar("Eva"))
            resposta = await receber(leitor)

            assert resposta == Erro("mesa_cheia")
            assert servidor.nomes == ["Ana", "Bia", "Caio", "Duda"]
            await fechar((leitor, escritor), *conexoes)

    asyncio.run(cenario())


def test_nao_sentado_e_recusado() -> None:
    async def cenario() -> None:
        async with mesa() as (_, porta):
            leitor, escritor = await asyncio.open_connection("127.0.0.1", porta)
            await enviar(escritor, Jogar(Carta.de_texto("7H")))
            await enviar(escritor, Responder(True))

            assert await receber(leitor) == Erro("nao_sentado")
            assert await receber(leitor) == Erro("nao_sentado")

            ana, ana_escritor = await sentar(porta, "Ana")
            assert isinstance(await receber(ana), Estado)
            await fechar((leitor, escritor), (ana, ana_escritor))

    asyncio.run(cenario())


def test_mensagem_de_direcao_errada_e_recusada() -> None:
    async def cenario() -> None:
        async with mesa() as (servidor, porta):
            leitor, escritor = await sentar(porta, "Ana")
            await receber(leitor)
            await enviar(escritor, Estado(assentos=[None, None, None, None], mao=[]))
            await enviar(escritor, Erro("qualquer"))

            assert await receber(leitor) == Erro("mensagem_invalida")
            assert await receber(leitor) == Erro("mensagem_invalida")
            assert servidor.nomes == ["Ana", None, None, None]
            await fechar((leitor, escritor))

    asyncio.run(cenario())


def test_quatro_assentos_abrem_a_pergunta_cima_ou_baixo() -> None:
    async def cenario() -> None:
        async with mesa() as (_, porta):
            primeiros = [await sentar(porta, nome) for nome in ("Ana", "Bia", "Caio")]
            quarto = await sentar(porta, "Duda")
            snapshots = [await drenar(leitor) for leitor, _ in (quarto, *primeiros)]

            for snapshot in snapshots:
                assert isinstance(snapshot, Estado)
                assert snapshot.assentos == ["Ana", "Bia", "Caio", "Duda"]
                assert snapshot.respondente == 1
                assert snapshot.trunfo is None
            await fechar(quarto, *primeiros)

    asyncio.run(cenario())


def test_responder_prepara_a_mao_e_distribui_dez_cartas() -> None:
    async def cenario() -> None:
        async with mesa() as (_, porta):
            conexoes = await sentar_quatro(porta)
            respondente = (await drenar(conexoes[0][0])).respondente
            assert respondente is not None

            await enviar(conexoes[respondente][1], Responder(True))
            snapshots = [await drenar(leitor) for leitor, _ in conexoes]

            for snapshot in snapshots:
                assert snapshot.assentos == ["Ana", "Bia", "Caio", "Duda"]
                assert len(snapshot.mao) == 10
                assert snapshot.contagens == [10, 10, 10, 10]
                assert snapshot.trunfo is not None
                assert snapshot.vez == 0
            await fechar(*conexoes)

    asyncio.run(cenario())


def test_responder_fora_de_hora_e_recusado() -> None:
    async def cenario() -> None:
        async with mesa() as (servidor, porta):
            ana, ana_escritor = await sentar(porta, "Ana")
            await drenar(ana)
            await enviar(ana_escritor, Responder(True))

            assert isinstance(await receber(ana), Erro)

            outros = [await sentar(porta, nome) for nome in ("Bia", "Caio", "Duda")]
            conexoes = [(ana, ana_escritor), *outros]
            inicial = await drenar(ana)
            respondente = inicial.respondente
            assert respondente is not None

            await enviar(conexoes[respondente][1], Responder(True))
            snapshots = [await drenar(leitor) for leitor, _ in conexoes]
            preparado = snapshots[0].carta_trunfo
            assert preparado is not None

            await enviar(conexoes[respondente][1], Responder(False))
            assert isinstance(await receber(conexoes[respondente][0]), Erro)
            assert servidor.jogo.mao.carta_trunfo is not None
            assert servidor.jogo.mao.carta_trunfo.texto() == preparado
            await fechar(*conexoes)

    asyncio.run(cenario())


def test_jogada_ilegal_vira_erro_so_para_quem_jogou() -> None:
    async def cenario() -> None:
        async with mesa() as (servidor, porta):
            conexoes, snapshots = await mesa_pronta(porta)
            vez = snapshots[0].vez
            assert vez is not None
            fora = (vez + 1) % 4

            await enviar(conexoes[fora][1], Jogar(Carta.de_texto(snapshots[fora].mao[0])))

            assert await receber(conexoes[fora][0]) == Erro("fora_da_vez")
            for i, (leitor, _) in enumerate(conexoes):
                if i != fora:
                    await nada(leitor)
            assert servidor.jogo.mao.vez == vez
            await fechar(*conexoes)

    asyncio.run(cenario())


def test_jogada_legal_chega_aos_quatro() -> None:
    async def cenario() -> None:
        async with mesa() as (_, porta):
            conexoes, snapshots = await mesa_pronta(porta)
            vez = snapshots[0].vez
            assert vez is not None
            carta = snapshots[vez].mao[0]

            await enviar(conexoes[vez][1], Jogar(Carta.de_texto(carta)))

            for assento, (leitor, _) in enumerate(conexoes):
                snapshot = await drenar(leitor)
                assert snapshot.vaza == [(vez, carta)]
                assert len(snapshot.mao) == (9 if assento == vez else 10)
                assert snapshot.contagens == [10 if i != vez else 9 for i in range(4)]
                assert snapshot.vez == (vez + 1) % 4
            await fechar(*conexoes)

    asyncio.run(cenario())

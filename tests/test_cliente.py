"""Testes do cliente TUI — tela, teclas e linha de comando (sprint 06)."""

from __future__ import annotations

import asyncio
import socket
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any

import pytest
from textual.widgets import Static
from textual.widgets._footer import FooterKey

from pysueca.carta import Carta
from pysueca.main import (
    RespostaScreen,
    SuecaApp,
    analisar,
    desenhar_assentos,
    desenhar_carta,
    desenhar_mesa,
    frase_do_motivo,
)
from pysueca.motor import ErroJogada
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
from pysueca.servidor import analisar as analisar_servidor

TIMEOUT = 1.0


class ServidorFalso:
    """Servidor roteirizado: grava as intenções e manda os snapshots pedidos."""

    def __init__(self) -> None:
        self.porta = 0
        self.recebidas: asyncio.Queue[Mensagem] = asyncio.Queue()
        self.escritores: list[asyncio.StreamWriter] = []

    async def atender(
        self, leitor: asyncio.StreamReader, escritor: asyncio.StreamWriter
    ) -> None:
        self.escritores.append(escritor)
        while True:
            linha = await leitor.readline()
            if not linha:
                break
            await self.recebidas.put(desserializar(linha))

    async def proxima(self) -> Mensagem:
        """A próxima intenção do cliente, com timeout curto."""
        return await asyncio.wait_for(self.recebidas.get(), TIMEOUT)

    async def enviar(self, mensagem: Mensagem) -> None:
        """Manda a mensagem aos clientes conectados."""
        await self.enviar_cru(serializar(mensagem))

    async def enviar_cru(self, linha: bytes) -> None:
        """Manda uma linha qualquer, para o caso de fio malformado."""
        for escritor in self.escritores:
            escritor.write(linha)
        for escritor in self.escritores:
            await escritor.drain()

    async def fechar(self) -> None:
        """Fecha a conexão, simulando o servidor que cai."""
        for escritor in self.escritores:
            escritor.close()
        for escritor in self.escritores:
            await escritor.wait_closed()


@asynccontextmanager
async def servidor_falso() -> AsyncIterator[ServidorFalso]:
    """O servidor falso escutando em `127.0.0.1` na porta efêmera."""
    falso = ServidorFalso()
    tcp = await asyncio.start_server(falso.atender, "127.0.0.1", 0)
    falso.porta = tcp.sockets[0].getsockname()[1]
    try:
        yield falso
    finally:
        tcp.close()
        for escritor in falso.escritores:
            escritor.close()


def porta_livre() -> int:
    """Uma porta TCP livre para o cenário sem servidor."""
    with socket.socket() as sonda:
        sonda.bind(("127.0.0.1", 0))
        return sonda.getsockname()[1]


type Cenario = Callable[[SuecaApp, Any, ServidorFalso], Awaitable[None]]


def rodar(nome: str, cenario: Cenario) -> None:
    """Sobe o servidor falso, monta o app headless e roda o cenário."""

    async def interno() -> None:
        async with servidor_falso() as falso:
            app = SuecaApp("127.0.0.1", falso.porta, nome)
            async with app.run_test() as pilot:
                await cenario(app, pilot, falso)

    asyncio.run(interno())


def rodar_sem_servidor(
    nome: str, cenario: Callable[[SuecaApp, Any], Awaitable[None]]
) -> None:
    """Roda o cenário com a porta fechada: nenhum servidor escutando."""

    async def interno() -> None:
        app = SuecaApp("127.0.0.1", porta_livre(), nome)
        async with app.run_test() as pilot:
            await cenario(app, pilot)

    asyncio.run(interno())


def painel(app: SuecaApp, seletor: str) -> str:
    """O texto renderizado do painel."""
    return app.query_one(seletor, Static).render().plain


def indice_destacado(app: SuecaApp) -> int | None:
    """O índice da carta com o realce `reverse`, lido dos spans da mão."""
    for span in app.query_one("#mao", Static).render().spans:
        if "reverse" in str(span.style):
            return span.start // 3
    return None


async def aguardar(pilot: Any, condicao: Callable[[], bool]) -> None:
    """Processa eventos até a condição valer, sem depender do relógio."""
    for _ in range(200):
        await pilot.pause()
        if condicao():
            return
    raise AssertionError("a tela não chegou ao estado esperado")


def test_o_cliente_manda_entrar_com_o_nome() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")

    rodar("Ana", cenario)


def test_tela_de_espera_mostra_n_de_4_assentos() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(Estado(assentos=["Ana", "Bia", None, None], mao=[]))
        await aguardar(pilot, lambda: "2 de 4" in painel(app, "#assentos"))
        texto = painel(app, "#assentos")
        assert "Ana" in texto
        assert "Bia" in texto
        assert "vago" in texto
        await pilot.press("enter")
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(falso.recebidas.get(), 0.1)

    rodar("Ana", cenario)


def test_a_mao_desenha_as_cartas_com_o_naipe_colorido() -> None:
    assert desenhar_carta("7H") == "[red]7♥[/red]"
    assert desenhar_carta("AD") == "[red]A♦[/red]"
    assert desenhar_carta("7C") == "7♣"
    assert desenhar_carta("AS") == "A♠"


def test_a_mesa_mostra_trunfo_vaza_e_placar() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H"],
                carta_trunfo="AH",
                vaza=[(0, "7H"), (1, "AC")],
                partidas=[1, 2],
            )
        )
        await aguardar(pilot, lambda: "A♥" in painel(app, "#mesa"))
        mesa = painel(app, "#mesa")
        assert "A♥" in mesa
        assert "7♥" in mesa
        assert "A♣" in mesa
        assert "Ana" in mesa
        assert "Bia" in mesa
        assert "1 x 2" in mesa

    rodar("Ana", cenario)


def test_a_mesa_desenha_a_vaza_vazia_e_a_vaza_cheia() -> None:
    vazia = desenhar_mesa(
        Estado(assentos=["Ana", "Bia", "Caio", "Duda"], mao=[], carta_trunfo="AH")
    )
    assert vazia.splitlines() == ["Trunfo: [red]A♥[/red]", "Placar: 0 x 0"]

    cheia = desenhar_mesa(
        Estado(
            assentos=["Ana", "Bia", "Caio", "Duda"],
            mao=[],
            carta_trunfo="7C",
            vaza=[(0, "7H"), (1, "7C"), (2, "7S"), (3, "7D")],
            partidas=[1, 2],
        )
    )
    assert cheia.splitlines() == [
        "Trunfo: 7♣",
        "Ana: [red]7♥[/red]",
        "Bia: 7♣",
        "Caio: 7♠",
        "Duda: [red]7♦[/red]",
        "Placar: 1 x 2",
    ]


def test_todo_codigo_de_motivo_do_v1_vira_frase_de_jogador() -> None:
    motivos = [erro.value for erro in ErroJogada] + [
        "mensagem_invalida",
        "nome_em_uso",
        "mesa_cheia",
        "nao_sentado",
        "mesa_congelada",
        "mesa_incompleta",
        "fora_de_hora",
        "json_invalido",
        "tipo_desconhecido",
        "campo_extra",
        "campo_faltando",
        "campo_invalido",
        "nome_invalido",
    ]
    generica = frase_do_motivo("motivo_inventado")
    for motivo in motivos:
        frase = frase_do_motivo(motivo)
        assert frase
        assert frase != motivo
        assert "_" not in frase
        assert frase != generica


def test_motivo_desconhecido_nao_vaza_codigo_nem_derruba_a_tela() -> None:
    frase = frase_do_motivo("bug_novo")
    assert frase == "A mesa recusou o pedido"
    assert "bug_novo" not in frase

    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(Erro("bug_novo"))
        await aguardar(pilot, lambda: "recusou o pedido" in painel(app, "#aviso"))
        assert "bug_novo" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_o_fim_do_jogo_aparece_na_mesa() -> None:
    mesa = desenhar_mesa(
        Estado(
            assentos=["Ana", "Bia", "Caio", "Duda"],
            mao=[],
            carta_trunfo="AH",
            partidas=[4, 2],
            encerrado=True,
            vencedor=0,
        )
    )
    assert "Fim de jogo" in mesa
    assert "Ana e Caio" in mesa
    assert "4 x 2" in mesa


def test_o_jogo_em_andamento_segue_mostrando_o_placar_simples() -> None:
    mesa = desenhar_mesa(
        Estado(assentos=["Ana", "Bia", "Caio", "Duda"], mao=[], partidas=[1, 2])
    )
    assert "Placar: 1 x 2" in mesa
    assert "Fim de jogo" not in mesa


def test_a_mesa_encerrada_nao_anuncia_vez() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=[],
                vez=0,
                partidas=[4, 2],
                encerrado=True,
                vencedor=0,
            )
        )
        await aguardar(pilot, lambda: "4 de 4" in painel(app, "#assentos"))
        assert "Sua vez" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_a_mesa_encerrada_nao_manda_jogar() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H", "AC"],
                vez=0,
                partidas=[4, 2],
                encerrado=True,
                vencedor=0,
            )
        )
        await aguardar(pilot, lambda: painel(app, "#mao") != "")
        await pilot.press("enter")
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(falso.recebidas.get(), 0.1)
        assert "Não é a sua vez" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_o_nome_ausente_cai_para_a_dupla() -> None:
    mesa = desenhar_mesa(
        Estado(
            assentos=["Ana", "Bia", "Caio", None],
            mao=[],
            partidas=[2, 4],
            encerrado=True,
            vencedor=1,
        )
    )
    assert "dupla 1–3" in mesa
    assert "None" not in mesa


def test_os_assentos_mostram_a_contagem_de_cartas() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H"],
                contagens=[10, 9, 10, 10],
            )
        )
        await aguardar(pilot, lambda: "Bia: 9" in painel(app, "#assentos"))
        assentos = painel(app, "#assentos")
        assert "Ana: 10" in assentos
        assert "Caio: 10" in assentos
        assert "Duda: 10" in assentos

    rodar("Ana", cenario)


def test_os_assentos_contam_os_nomes_com_um_assento_vago_no_meio() -> None:
    texto = desenhar_assentos(
        Estado(assentos=["Ana", None, "Caio", "Duda"], mao=[], contagens=[10, 0, 9, 10])
    )
    assert texto.splitlines() == [
        "3 de 4",
        "Ana: 10",
        "assento 1: vago",
        "Caio: 9",
        "Duda: 10",
    ]


def test_setas_movem_a_selecao_e_enter_joga_a_carta() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H", "AC", "QS"],
                vez=0,
            )
        )
        await aguardar(pilot, lambda: painel(app, "#mao") != "")
        assert indice_destacado(app) == 0
        await pilot.press("right")
        await pilot.pause()
        assert indice_destacado(app) == 1
        await pilot.press("enter")
        assert await falso.proxima() == Jogar(Carta.de_texto("AC"))

    rodar("Ana", cenario)


def test_a_selecao_nao_passa_dos_limites_da_mao() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H", "AC", "QS"],
                vez=0,
            )
        )
        await aguardar(pilot, lambda: painel(app, "#mao") != "")
        await pilot.press("left")
        await pilot.pause()
        assert indice_destacado(app) == 0
        for _ in range(4):
            await pilot.press("right")
            await pilot.pause()
        assert indice_destacado(app) == 2
        await pilot.press("enter")
        assert await falso.proxima() == Jogar(Carta.de_texto("QS"))

    rodar("Ana", cenario)


def test_fora_da_vez_o_servidor_decide() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H", "AC"],
                vez=1,
            )
        )
        await aguardar(pilot, lambda: painel(app, "#mao") != "")
        await pilot.press("enter")
        assert await falso.proxima() == Jogar(Carta.de_texto("7H"))
        await falso.enviar(Erro("fora_de_hora"))
        await aguardar(
            pilot, lambda: "não esperava essa jogada" in painel(app, "#aviso")
        )
        assert "A mesa não esperava essa jogada agora" in painel(app, "#aviso")
        assert "fora_de_hora" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_a_selecao_volta_a_primeira_carta_com_a_mao_nova() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H", "AC", "QS"],
                vez=0,
            )
        )
        await aguardar(pilot, lambda: painel(app, "#mao") != "")
        await pilot.press("right")
        await pilot.press("right")
        await pilot.pause()
        assert indice_destacado(app) == 2
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["AD", "KC"],
                vez=0,
            )
        )
        await aguardar(pilot, lambda: "A♦" in painel(app, "#mao"))
        assert indice_destacado(app) == 0
        await pilot.press("enter")
        assert await falso.proxima() == Jogar(Carta.de_texto("AD"))

    rodar("Ana", cenario)


def test_com_a_mao_vazia_nada_e_jogado() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await pilot.press("left")
        await pilot.press("right")
        await pilot.pause()
        assert app.selecao == 0
        await falso.enviar(Estado(assentos=["Ana", "Bia", None, None], mao=[]))
        await aguardar(pilot, lambda: "2 de 4" in painel(app, "#assentos"))
        await pilot.press("left")
        await pilot.press("right")
        await pilot.pause()
        assert app.selecao == 0
        await pilot.press("enter")
        with pytest.raises(TimeoutError):
            await asyncio.wait_for(falso.recebidas.get(), 0.1)

    rodar("Ana", cenario)


def test_cima_ou_baixo_abre_na_tela_do_respondente() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(assentos=["Bia", "Ana", "Caio", "Duda"], mao=[], respondente=1)
        )
        await aguardar(pilot, lambda: isinstance(app.screen, RespostaScreen))
        assert isinstance(app.screen, RespostaScreen)

    rodar("Ana", cenario)


def test_cima_ou_baixo_responde() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(assentos=["Bia", "Ana", "Caio", "Duda"], mao=[], respondente=1)
        )
        await aguardar(pilot, lambda: isinstance(app.screen, RespostaScreen))
        await pilot.press("c")
        assert await falso.proxima() == Responder(True)
        await aguardar(pilot, lambda: not isinstance(app.screen, RespostaScreen))
        assert not isinstance(app.screen, RespostaScreen)
        await falso.enviar(
            Estado(assentos=["Bia", "Ana", "Caio", "Duda"], mao=[], respondente=1)
        )
        await aguardar(pilot, lambda: isinstance(app.screen, RespostaScreen))
        await pilot.press("b")
        assert await falso.proxima() == Responder(False)
        await aguardar(pilot, lambda: not isinstance(app.screen, RespostaScreen))
        assert not isinstance(app.screen, RespostaScreen)

    rodar("Ana", cenario)


def test_quem_nao_e_o_respondente_nao_ve_o_dialogo() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(assentos=["Bia", "Ana", "Caio", "Duda"], mao=[], respondente=2)
        )
        await aguardar(pilot, lambda: painel(app, "#assentos") != "")
        assert not isinstance(app.screen, RespostaScreen)
        await falso.enviar(
            Estado(assentos=["Bia", "Ana", "Caio", "Duda"], mao=[], respondente=1)
        )
        await aguardar(pilot, lambda: isinstance(app.screen, RespostaScreen))
        await falso.enviar(
            Estado(
                assentos=["Bia", "Ana", "Caio", "Duda"],
                mao=["7H"],
                trunfo="H",
                carta_trunfo="AH",
            )
        )
        await aguardar(pilot, lambda: not isinstance(app.screen, RespostaScreen))
        assert not isinstance(app.screen, RespostaScreen)

    rodar("Ana", cenario)


def test_a_queda_aparece_na_tela() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H"],
                ausentes=[2],
            )
        )
        await aguardar(pilot, lambda: "congelada" in painel(app, "#aviso"))
        assert "Caio" in painel(app, "#aviso")
        assert "7♥" in painel(app, "#mao")

    rodar("Ana", cenario)


def test_reconexao_limpa_a_tela_de_queda() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H"],
                ausentes=[2],
            )
        )
        await aguardar(pilot, lambda: "congelada" in painel(app, "#aviso"))
        await falso.enviar(Estado(assentos=["Ana", "Bia", "Caio", "Duda"], mao=["7H"]))
        await aguardar(pilot, lambda: "congelada" not in painel(app, "#aviso"))
        assert "congelada" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_erro_do_servidor_aparece_sem_derrubar_o_app() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(Estado(assentos=["Ana", None, None, None], mao=[]))
        await aguardar(pilot, lambda: "1 de 4" in painel(app, "#assentos"))
        await falso.enviar(Erro("nome_em_uso"))
        await aguardar(pilot, lambda: "já está em uso" in painel(app, "#aviso"))
        assert "Esse nome já está em uso nesta mesa" in painel(app, "#aviso")
        assert "nome_em_uso" not in painel(app, "#aviso")
        await falso.enviar(Estado(assentos=["Ana", "Bia", None, None], mao=[]))
        await aguardar(pilot, lambda: "2 de 4" in painel(app, "#assentos"))
        assert "já está em uso" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_mensagem_invalida_do_fio_nao_derruba_o_app() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar_cru(b"isto nao e json\n")
        await aguardar(pilot, lambda: "não deu para ler" in painel(app, "#aviso"))
        assert "A mesa mandou uma mensagem que não deu para ler" in painel(app, "#aviso")
        assert "json_invalido" not in painel(app, "#aviso")
        await falso.enviar(Estado(assentos=["Ana", "Bia", None, None], mao=[]))
        await aguardar(pilot, lambda: "2 de 4" in painel(app, "#assentos"))
        assert "não deu para ler" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_sem_servidor_o_cliente_avisa_e_segue() -> None:
    async def cenario(app: SuecaApp, pilot: Any) -> None:
        await aguardar(pilot, lambda: "conexão" in painel(app, "#aviso"))
        assert "conexão" in painel(app, "#aviso")

    rodar_sem_servidor("Ana", cenario)


def test_o_fim_da_conexao_vira_aviso() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(Estado(assentos=["Ana", None, None, None], mao=[]))
        await aguardar(pilot, lambda: "1 de 4" in painel(app, "#assentos"))
        await falso.fechar()
        await aguardar(pilot, lambda: "Conexão encerrada" in painel(app, "#aviso"))
        assert "Conexão encerrada" in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_o_teto_do_leitor_vira_aviso() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar_cru(b"x" * 70000 + b"\n")
        await aguardar(pilot, lambda: "Conexão encerrada" in painel(app, "#aviso"))
        assert "Conexão encerrada" in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_o_cliente_se_reconhece_pelo_nome() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(Estado(assentos=["Bia", "Ana", None, None], mao=[], vez=1))
        await aguardar(pilot, lambda: "Sua vez" in painel(app, "#aviso"))
        assert "Sua vez" in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_congelado_o_cliente_ainda_manda_e_o_servidor_recusa() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")
        await falso.enviar(
            Estado(
                assentos=["Ana", "Bia", "Caio", "Duda"],
                mao=["7H", "AC"],
                ausentes=[2],
            )
        )
        await aguardar(pilot, lambda: "congelada" in painel(app, "#aviso"))
        await pilot.press("enter")
        assert await falso.proxima() == Jogar(Carta.de_texto("7H"))
        await falso.enviar(Erro("mesa_congelada"))
        await aguardar(pilot, lambda: "a jogada não valeu" in painel(app, "#aviso"))
        assert "A mesa está congelada: a jogada não valeu" in painel(app, "#aviso")
        assert "mesa_congelada" not in painel(app, "#aviso")

    rodar("Ana", cenario)


def test_as_teclas_de_jogo_aparecem_no_rodape() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        await pilot.pause()
        visiveis = {
            (tecla.key_display, tecla.description)
            for tecla in app.query(FooterKey)
            if tecla.display
        }
        assert ("←", "Anterior") in visiveis
        assert ("→", "Próxima") in visiveis
        assert ("⏎", "Jogar") in visiveis
        assert ("^q", "Sair") in visiveis

    rodar("Ana", cenario)


def test_d_alterna_o_tema() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        await pilot.pause()
        visiveis = {
            (tecla.key_display, tecla.description)
            for tecla in app.query(FooterKey)
            if tecla.display
        }
        assert ("d", "Tema") in visiveis
        assert app.theme == "textual-dark"
        await pilot.press("d")
        await pilot.pause()
        assert app.theme == "textual-light"
        await pilot.press("d")
        await pilot.pause()
        assert app.theme == "textual-dark"

    rodar("Ana", cenario)


def test_o_cliente_le_nome_host_e_porta() -> None:
    args = analisar(["Ana", "--host", "10.0.0.2", "--porta", "9000"])
    assert args.nome == "Ana"
    assert args.host == "10.0.0.2"
    assert args.porta == 9000


def test_o_cliente_usa_os_defaults() -> None:
    args = analisar(["Ana"])
    assert args.host == "127.0.0.1"
    assert args.porta == 8765


def test_o_servidor_le_host_e_porta() -> None:
    args = analisar_servidor(["--porta", "9000"])
    assert args.host == "127.0.0.1"
    assert args.porta == 9000


def test_o_servidor_usa_a_porta_default() -> None:
    args = analisar_servidor([])
    assert args.host == "127.0.0.1"
    assert args.porta == 8765


def test_argumento_desconhecido_sai_com_erro() -> None:
    with pytest.raises(SystemExit) as saida:
        analisar(["Ana", "--turbo"])
    assert saida.value.code != 0

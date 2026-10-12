"""Testes do servidor — assentos, intenções e broadcast (sprint 05)."""

import asyncio
from contextlib import asynccontextmanager

from pysueca.protocolo import (
    Entrar,
    Erro,
    Estado,
    Mensagem,
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
            conexoes = [await sentar(porta, nome) for nome in ("Ana", "Bia", "Caio", "Duda")]
            for leitor, _ in conexoes:
                await receber(leitor)

            leitor, escritor = await asyncio.open_connection("127.0.0.1", porta)
            await enviar(escritor, Entrar("Ana"))
            resposta = await receber(leitor)

            assert resposta == Erro("nome_em_uso")
            assert servidor.nomes == ["Ana", "Bia", "Caio", "Duda"]
            await fechar((leitor, escritor), *conexoes)

    asyncio.run(cenario())

"""Testes do servidor — assentos, intenções e broadcast (sprint 05)."""

import asyncio
from contextlib import asynccontextmanager

from pysueca.protocolo import (
    Entrar,
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
        await tcp.wait_closed()


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


def test_entrar_senta_no_primeiro_assento_livre() -> None:
    async def cenario() -> None:
        async with mesa() as (_, porta):
            leitor, escritor = await sentar(porta, "Ana")

            snapshot = await receber(leitor)

            assert isinstance(snapshot, Estado)
            assert snapshot.assentos == ["Ana", None, None, None]
            assert snapshot.mao == []
            assert snapshot.contagens == [0, 0, 0, 0]
            escritor.close()
            await escritor.wait_closed()

    asyncio.run(cenario())

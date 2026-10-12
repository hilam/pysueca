"""Testes do cliente TUI — tela, teclas e linha de comando (sprint 06)."""

from __future__ import annotations

import asyncio
import socket
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Awaitable, Callable

import pytest
from textual.widgets import Static

from pysueca.main import SuecaApp
from pysueca.protocolo import (
    Entrar,
    Estado,
    Mensagem,
    desserializar,
    serializar,
)

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
        for escritor in self.escritores:
            escritor.write(serializar(mensagem))
        for escritor in self.escritores:
            await escritor.drain()


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


def painel(app: SuecaApp, seletor: str) -> str:
    """O texto renderizado do painel."""
    return app.query_one(seletor, Static).render().plain


def test_o_cliente_manda_entrar_com_o_nome() -> None:
    async def cenario(app: SuecaApp, pilot: Any, falso: ServidorFalso) -> None:
        assert await falso.proxima() == Entrar("Ana")

    rodar("Ana", cenario)

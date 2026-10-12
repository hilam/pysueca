"""O servidor: dono do jogo e dos assentos — a única casca asyncio (sprint 05)."""

from __future__ import annotations

import asyncio

from pysueca.motor import Jogo
from pysueca.protocolo import (
    TETO_LINHA,
    Entrar,
    Mensagem,
    desserializar,
    estado,
    serializar,
)


class Servidor:
    """A mesa: o `Jogo` e os quatro assentos (nome e conexão)."""

    def __init__(self) -> None:
        self.nomes: list[str | None] = [None, None, None, None]
        self.conexoes: list[asyncio.StreamWriter | None] = [None, None, None, None]
        self.jogo = Jogo()

    async def iniciar(self, host: str, porta: int) -> asyncio.Server:
        """Sobe o servidor TCP com o teto do protocolo e devolve o `asyncio.Server`."""
        return await asyncio.start_server(self.atender, host, porta, limit=TETO_LINHA)

    async def atender(
        self, leitor: asyncio.StreamReader, escritor: asyncio.StreamWriter
    ) -> None:
        """O laço de uma conexão: uma intenção por linha."""
        try:
            while True:
                linha = await leitor.readline()
                if not linha:
                    break
                mensagem = desserializar(linha)
                if isinstance(mensagem, Entrar):
                    assento = self._sentar(mensagem.nome, escritor)
                    await self._enviar(escritor, estado(self.jogo, self.nomes, assento))
        finally:
            escritor.close()
            await escritor.wait_closed()

    def _sentar(self, nome: str, escritor: asyncio.StreamWriter) -> int:
        """Senta o nome no primeiro assento livre e devolve o assento."""
        assento = self.nomes.index(None)
        self.nomes[assento] = nome
        self.conexoes[assento] = escritor
        return assento

    async def _enviar(self, escritor: asyncio.StreamWriter, mensagem: Mensagem) -> None:
        escritor.write(serializar(mensagem))
        await escritor.drain()

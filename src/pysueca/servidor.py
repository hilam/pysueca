"""O servidor: dono do jogo e dos assentos — a única casca asyncio (sprint 05)."""

from __future__ import annotations

import asyncio

from pysueca.motor import Jogo
from pysueca.protocolo import (
    TETO_LINHA,
    Entrar,
    Erro,
    Estado,
    Jogar,
    Mensagem,
    Responder,
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
        assento: int | None = None
        try:
            while True:
                linha = await leitor.readline()
                if not linha:
                    break
                mensagem = desserializar(linha)
                if isinstance(mensagem, Entrar):
                    if self._em_uso(mensagem.nome):
                        await self._enviar(escritor, Erro("nome_em_uso"))
                        continue
                    if None not in self.nomes:
                        await self._enviar(escritor, Erro("mesa_cheia"))
                        continue
                    assento = self._sentar(mensagem.nome, escritor)
                    await self._transmitir()
                elif isinstance(mensagem, (Jogar, Responder)):
                    if assento is None:
                        await self._enviar(escritor, Erro("nao_sentado"))
                    elif isinstance(mensagem, Responder):
                        self.jogo.preparar(mensagem.cima)
                        await self._transmitir()
                elif isinstance(mensagem, (Estado, Erro)):
                    await self._enviar(escritor, Erro("mensagem_invalida"))
        finally:
            escritor.close()
            await escritor.wait_closed()

    def _sentar(self, nome: str, escritor: asyncio.StreamWriter) -> int:
        """Senta o nome no primeiro assento livre e devolve o assento."""
        assento = self.nomes.index(None)
        self.nomes[assento] = nome
        self.conexoes[assento] = escritor
        return assento

    def _em_uso(self, nome: str) -> bool:
        """Só a conexão viva bloqueia o nome; o assento reservado aceita o dono de volta."""
        return any(
            guardado == nome and conexao is not None
            for guardado, conexao in zip(self.nomes, self.conexoes)
        )

    async def _enviar(self, escritor: asyncio.StreamWriter, mensagem: Mensagem) -> None:
        escritor.write(serializar(mensagem))
        await escritor.drain()

    async def _transmitir(self) -> None:
        """Manda o snapshot de cada assento ocupado, montado antes do primeiro write."""
        linhas = [
            (conexao, serializar(estado(self.jogo, self.nomes, assento)))
            for assento, conexao in enumerate(self.conexoes)
            if conexao is not None
        ]
        for conexao, linha in linhas:
            conexao.write(linha)
        for conexao, _ in linhas:
            await conexao.drain()

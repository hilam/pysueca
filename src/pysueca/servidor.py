"""O servidor: dono do jogo e dos assentos — a única casca asyncio (sprint 05)."""

from __future__ import annotations

import argparse
import asyncio

from pysueca.carta import Carta
from pysueca.motor import Jogo
from pysueca.protocolo import (
    TETO_LINHA,
    Entrar,
    Erro,
    Estado,
    Jogar,
    LinhaLonga,
    Mensagem,
    Responder,
    desserializar,
    erro_de_jogada,
    estado,
    serializar,
)

VAZAS_POR_MAO = 10


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
                try:
                    linha = await leitor.readline()
                except ValueError, LinhaLonga:
                    break
                if not linha:
                    break
                assento = await self._despachar(assento, escritor, desserializar(linha))
        finally:
            escritor.close()
            await escritor.wait_closed()
            await self._desconectar(assento)

    async def _despachar(
        self, assento: int | None, escritor: asyncio.StreamWriter, mensagem: Mensagem
    ) -> int | None:
        """Trata a intenção e devolve o assento da conexão (novo, se sentou agora)."""
        if isinstance(mensagem, Entrar):
            novo = await self._entrar(mensagem.nome, escritor)
            return assento if novo is None else novo
        if isinstance(mensagem, Jogar):
            await self._jogar(assento, mensagem.carta, escritor)
        elif isinstance(mensagem, Responder):
            await self._responder(assento, mensagem.cima, escritor)
        elif isinstance(mensagem, (Estado, Erro)):
            await self._enviar(escritor, Erro("mensagem_invalida"))
        return assento

    async def _entrar(self, nome: str, escritor: asyncio.StreamWriter) -> int | None:
        """Senta o nome, retoma o assento reservado ou recusa; `None` se recusado."""
        if self._em_uso(nome):
            await self._enviar(escritor, Erro("nome_em_uso"))
            return None
        reservado = self._reservado(nome)
        if reservado is not None:
            self.conexoes[reservado] = escritor
        elif None in self.nomes:
            reservado = self._sentar(nome, escritor)
        else:
            await self._enviar(escritor, Erro("mesa_cheia"))
            return None
        await self._transmitir()
        return reservado

    async def _jogar(
        self, assento: int | None, carta: Carta, escritor: asyncio.StreamWriter
    ) -> None:
        """Valida a jogada pelo motor, recusa com erro ou transmite o snapshot."""
        if assento is None:
            await self._enviar(escritor, Erro("nao_sentado"))
            return
        if self._ausentes():
            await self._enviar(escritor, Erro("mesa_congelada"))
            return
        erro = self.jogo.jogar(assento, carta)
        if erro is not None:
            await self._enviar(escritor, erro_de_jogada(erro))
            return
        if len(self.jogo.mao.vazas) == VAZAS_POR_MAO:
            self.jogo.encerrar_mao()
        await self._transmitir()

    async def _responder(
        self, assento: int | None, cima: bool, escritor: asyncio.StreamWriter
    ) -> None:
        """Prepara a mão se a pergunta estiver pendente para este assento."""
        if assento is None:
            await self._enviar(escritor, Erro("nao_sentado"))
            return
        if self._ausentes():
            await self._enviar(escritor, Erro("mesa_congelada"))
            return
        if None in self.nomes:
            await self._enviar(escritor, Erro("mesa_incompleta"))
            return
        if self._respondente() != assento:
            await self._enviar(escritor, Erro("fora_de_hora"))
            return
        self.jogo.preparar(cima)
        await self._transmitir()

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

    def _reservado(self, nome: str) -> int | None:
        """O assento do nome cujo dono caiu, ou `None`."""
        return next(
            (
                assento
                for assento, guardado in enumerate(self.nomes)
                if guardado == nome and self.conexoes[assento] is None
            ),
            None,
        )

    def _respondente(self) -> int | None:
        """O assento que deve responder cima ou baixo, ou `None` com a mão preparada."""
        if getattr(self.jogo.mao, "carta_trunfo", None) is not None:
            return None
        return (self.jogo.embaralhador + 1) % 4

    async def _enviar(self, escritor: asyncio.StreamWriter, mensagem: Mensagem) -> None:
        escritor.write(serializar(mensagem))
        await escritor.drain()

    async def _transmitir(self) -> None:
        """Manda o snapshot de cada assento ocupado, montado antes do primeiro write."""
        linhas = [
            (
                conexao,
                serializar(estado(self.jogo, self.nomes, assento, self._ausentes())),
            )
            for assento, conexao in enumerate(self.conexoes)
            if conexao is not None
        ]
        for conexao, linha in linhas:
            conexao.write(linha)
        for conexao, _ in linhas:
            await conexao.drain()

    def _ausentes(self) -> list[int]:
        """Os assentos reservados cujo dono caiu (nome guardado, sem conexão)."""
        return [
            assento
            for assento, nome in enumerate(self.nomes)
            if nome is not None and self.conexoes[assento] is None
        ]

    async def _desconectar(self, assento: int | None) -> None:
        """Reserva o assento do dono que caiu e avisa a mesa; conexão anônima é no-op."""
        if assento is None:
            return
        self.conexoes[assento] = None
        await self._transmitir()


def analisar(argv: list[str] | None = None) -> argparse.Namespace:
    """O comando de linha do servidor: host e porta com defaults."""
    parser = argparse.ArgumentParser(prog="pysueca-servidor")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--porta", type=int, default=8765)
    return parser.parse_args(argv)


async def _servir(host: str, porta: int) -> None:
    """Sobe a mesa e a mantém de pé."""
    tcp = await Servidor().iniciar(host, porta)
    async with tcp:
        await tcp.serve_forever()


def main(argv: list[str] | None = None) -> None:
    """Sobe o servidor autoritativo, dono da mesa."""
    args = analisar(argv)
    asyncio.run(_servir(args.host, args.porta))

"""O cliente Textual: a tela do jogador e o worker que lê o fio (sprint 06)."""

from __future__ import annotations

import argparse
import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Static

from pysueca.protocolo import (
    Entrar,
    Erro,
    Estado,
    Jogar,
    LinhaLonga,
    Mensagem,
    Responder,
    desserializar,
    serializar,
)

HOST_PADRAO = "127.0.0.1"
PORTA_PADRAO = 8765
# o snapshot legítimo é < 1 KB; o teto aqui só evita o `ValueError` do readline
LIMITE_LEITURA = 65536


def desenhar_assentos(estado: Estado) -> str:
    """`N de 4`, os nomes sentados e os assentos vagos."""
    ocupados = [nome for nome in estado.assentos if nome is not None]
    linhas = [f"{len(ocupados)} de 4"]
    for assento, nome in enumerate(estado.assentos):
        linhas.append(nome if nome is not None else f"assento {assento}: vago")
    return "\n".join(linhas)


class RespostaScreen(ModalScreen[None]):
    """O diálogo cima ou baixo, aberto só para o respondente da mão."""

    BINDINGS = [
        Binding("c", "cima", "Cima"),
        Binding("b", "baixo", "Baixo"),
    ]

    def compose(self) -> ComposeResult:
        yield Static("Cima ou baixo? [c] cima · [b] baixo", id="pergunta")

    async def action_cima(self) -> None:
        await self._responder(True)

    async def action_baixo(self) -> None:
        await self._responder(False)

    async def _responder(self, cima: bool) -> None:
        app = self.app
        assert isinstance(app, SuecaApp)
        await app.enviar(Responder(cima))
        app.pop_screen()


class SuecaApp(App[None]):
    """A mesa do jogador: worker de fio, painéis e teclas."""

    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair", priority=True),
    ]

    def __init__(self, host: str, porta: int, nome: str) -> None:
        super().__init__()
        self.host = host
        self.porta = porta
        self.nome = nome
        self.estado: Estado | None = None
        self.aviso_erro: str | None = None
        self.escritor: asyncio.StreamWriter | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static("Conectando...", id="aviso")
            yield Static("", id="assentos")
            yield Static("", id="mesa")
            yield Static("", id="mao")
        yield Footer()

    def on_mount(self) -> None:
        self.ler_fio()

    @work(exclusive=True)
    async def ler_fio(self) -> None:
        """Conecta, senta com o nome e lê o fio até o fim num só caminho."""
        try:
            leitor, escritor = await asyncio.open_connection(
                self.host, self.porta, limit=LIMITE_LEITURA
            )
        except OSError as erro:
            self.avisar(f"Sem conexão: {erro}")
            return
        self.escritor = escritor
        try:
            await self.enviar(Entrar(self.nome))
            while True:
                try:
                    linha = await leitor.readline()
                except (ValueError, LinhaLonga):
                    break
                if not linha:
                    break
                self._traduzir(desserializar(linha))
        finally:
            self.escritor = None
            escritor.close()
            await escritor.wait_closed()
            if self.is_running:
                self.avisar("Conexão encerrada")

    async def enviar(self, mensagem: Mensagem) -> None:
        """Escreve a intenção no fio, se a conexão existir."""
        if self.escritor is None:
            return
        self.escritor.write(serializar(mensagem))
        await self.escritor.drain()

    def _traduzir(self, mensagem: Mensagem) -> None:
        """Traduz a mensagem do fio em chamada de tela — o único ponto que muda."""
        if isinstance(mensagem, Estado):
            self.mostrar_estado(mensagem)
        elif isinstance(mensagem, Erro):
            self.avisar(mensagem.motivo)

    def mostrar_estado(self, estado: Estado) -> None:
        """Guarda o snapshot: a tela é uma função dele."""
        self.estado = estado
        self.aviso_erro = None
        self.query_one("#assentos", Static).update(desenhar_assentos(estado))

    def avisar(self, motivo: str) -> None:
        """Guarda o aviso de erro até o próximo snapshot."""
        self.aviso_erro = motivo


def analisar(argv: list[str] | None = None) -> argparse.Namespace:
    """O comando de linha do cliente: nome obrigatório, host e porta com defaults."""
    parser = argparse.ArgumentParser(prog="pysueca")
    parser.add_argument("nome")
    parser.add_argument("--host", default=HOST_PADRAO)
    parser.add_argument("--porta", type=int, default=PORTA_PADRAO)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Sobe a tela do cliente."""
    args = analisar(argv)
    SuecaApp(args.host, args.porta, args.nome).run()


if __name__ == "__main__":
    main()

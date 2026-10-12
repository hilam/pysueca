"""O cliente Textual: a tela do jogador e o worker que lê o fio (sprint 06)."""

from __future__ import annotations

import argparse
import asyncio
from typing import ClassVar

from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Static

from pysueca.carta import Carta, Naipe
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

SIMBOLOS = {Naipe.PAUS: "♣", Naipe.COPAS: "♥", Naipe.ESPADAS: "♠", Naipe.OUROS: "♦"}
VERMELHOS = frozenset({Naipe.COPAS, Naipe.OUROS})

# todo código de motivo do v1 (motor, servidor e forma do fio) em frase de jogador
MOTIVOS = {
    "fora_da_vez": "Não é a sua vez",
    "carta_fora_da_mao": "Essa carta não está na sua mão",
    "nao_seguiu_naipe": "Você precisa seguir o naipe puxado",
    "mensagem_invalida": "A mesa não entendeu a mensagem",
    "nome_em_uso": "Esse nome já está em uso nesta mesa",
    "mesa_cheia": "A mesa já tem quatro jogadores",
    "nao_sentado": "Você ainda não está sentado nesta mesa",
    "mesa_congelada": "A mesa está congelada: a jogada não valeu",
    "mesa_incompleta": "A mesa ainda não tem quatro jogadores",
    "fora_de_hora": "A mesa não esperava essa jogada agora",
    "json_invalido": "A mesa mandou uma mensagem que não deu para ler",
    "tipo_desconhecido": "A mesa mandou uma mensagem de tipo desconhecido",
    "campo_extra": "A mensagem da mesa trouxe um campo a mais",
    "campo_faltando": "A mensagem da mesa veio sem um campo",
    "campo_invalido": "A mensagem da mesa trouxe um valor inválido",
    "nome_invalido": "Esse nome não serve: use de 1 a 20 caracteres",
}
RECUSA_GENERICA = "A mesa recusou o pedido"


def frase_do_motivo(motivo: str) -> str:
    """O motivo de recusa do fio em frase de jogador; motivo novo cai no genérico."""
    return MOTIVOS.get(motivo, RECUSA_GENERICA)


def desenhar_carta(texto: str, destaque: bool = False) -> str:
    """A carta em markup do Textual, com copas e ouros em vermelho."""
    carta = Carta.de_texto(texto)
    markup = f"{carta.valor.value}{SIMBOLOS[carta.naipe]}"
    if carta.naipe in VERMELHOS:
        markup = f"[red]{markup}[/red]"
    if destaque:
        markup = f"[reverse]{markup}[/reverse]"
    return markup


def desenhar_mao(mao: list[str], selecao: int) -> str:
    """A mão inteira em uma linha, com a carta selecionada destacada."""
    return " ".join(
        desenhar_carta(texto, indice == selecao) for indice, texto in enumerate(mao)
    )


def desenhar_mesa(estado: Estado) -> str:
    """A carta do trunfo, a vaza corrente, o placar das duplas e o fim do jogo."""
    linhas = [
        f"Trunfo: {desenhar_carta(estado.carta_trunfo)}"
        if estado.carta_trunfo is not None
        else "Trunfo: —"
    ]
    for assento, texto in estado.vaza:
        nome = estado.assentos[assento] or f"assento {assento}"
        linhas.append(f"{nome}: {desenhar_carta(texto)}")
    partidas = estado.partidas if len(estado.partidas) >= 2 else [0, 0]
    if estado.encerrado and estado.vencedor is not None:
        linhas.append(f"Fim de jogo — venceu {nome_da_dupla(estado, estado.vencedor)}")
    linhas.append(f"Placar: {partidas[0]} x {partidas[1]}")
    return "\n".join(linhas)


def nome_da_dupla(estado: Estado, dupla: int) -> str:
    """Os dois nomes da dupla quando existem; senão os próprios assentos."""
    assentos = (0, 2) if dupla == 0 else (1, 3)
    nomes = [estado.assentos[assento] for assento in assentos]
    if all(nomes):
        return f"{nomes[0]} e {nomes[1]}"
    return f"dupla {assentos[0]}–{assentos[1]}"


def desenhar_assentos(estado: Estado) -> str:
    """`N de 4`, os nomes sentados e os assentos vagos."""
    ocupados = [nome for nome in estado.assentos if nome is not None]
    linhas = [f"{len(ocupados)} de 4"]
    for assento, nome in enumerate(estado.assentos):
        if nome is None:
            linhas.append(f"assento {assento}: vago")
        else:
            contagem = (
                estado.contagens[assento] if assento < len(estado.contagens) else 0
            )
            linhas.append(f"{nome}: {contagem}")
    return "\n".join(linhas)


class RespostaScreen(ModalScreen[None]):
    """O diálogo cima ou baixo, aberto só para o respondente da mão."""

    BINDINGS: ClassVar[list[BindingType]] = [
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

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("ctrl+q", "quit", "Sair", priority=True),
        Binding("left", "selecionar(-1)", "Anterior"),
        Binding("right", "selecionar(1)", "Próxima"),
        Binding("enter", "jogar", "Jogar"),
    ]

    def __init__(self, host: str, porta: int, nome: str) -> None:
        super().__init__()
        self.host = host
        self.porta = porta
        self.nome = nome
        self.estado: Estado | None = None
        self.aviso_erro: str | None = None
        self.selecao = 0
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

    @property
    def meu_assento(self) -> int | None:
        """O próprio assento, derivado do nome no snapshot (o nome é único)."""
        if self.estado is None or self.nome not in self.estado.assentos:
            return None
        return self.estado.assentos.index(self.nome)

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
                except ValueError, LinhaLonga:
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
            # o código do fio morre aqui: daqui para a tela só desce frase de jogador
            self.avisar(frase_do_motivo(mensagem.motivo))

    def action_selecionar(self, delta: int) -> None:
        """Move a seleção dentro da mão, sem passar dos limites."""
        if not self.estado or not self.estado.mao:
            return
        self.selecao = max(0, min(self.selecao + delta, len(self.estado.mao) - 1))
        self.desenhar_mao_painel()

    async def action_jogar(self) -> None:
        """Manda a carta selecionada; quem decide se a jogada vale é o servidor."""
        if not self.estado or not self.estado.mao or self.estado.encerrado:
            return
        await self.enviar(Jogar(Carta.de_texto(self.estado.mao[self.selecao])))

    def mostrar_estado(self, estado: Estado) -> None:
        """Guarda o snapshot: a tela é uma função dele."""
        if self.estado is None or self.estado.mao != estado.mao:
            self.selecao = 0
        self.estado = estado
        self.aviso_erro = None
        self.desenhar_tela()

    def desenhar_tela(self) -> None:
        """Redesenha todos os painéis a partir do estado corrente."""
        estado = self.estado
        assert estado is not None
        self.query_one("#assentos", Static).update(desenhar_assentos(estado))
        self.query_one("#mesa", Static).update(desenhar_mesa(estado))
        self.desenhar_mao_painel()
        self.desenhar_aviso()
        self._sincronizar_pergunta()

    def desenhar_mao_painel(self) -> None:
        """Redesenha a mão com a seleção corrente."""
        if self.estado is not None:
            self.query_one("#mao", Static).update(
                desenhar_mao(self.estado.mao, self.selecao)
            )

    def _sincronizar_pergunta(self) -> None:
        """Abre o cima ou baixo só para o respondente e fecha quando a pergunta passa."""
        estado = self.estado
        deve_abrir = (
            estado is not None
            and estado.trunfo is None
            and estado.respondente is not None
            and estado.respondente == self.meu_assento
        )
        aberto = isinstance(self.screen, RespostaScreen)
        if deve_abrir and not aberto:
            self.push_screen(RespostaScreen())
        elif not deve_abrir and aberto:
            self.pop_screen()

    def avisar(self, motivo: str) -> None:
        """Guarda o aviso de erro até o próximo snapshot."""
        self.aviso_erro = motivo
        self.desenhar_aviso()

    def texto_aviso(self) -> str:
        """O aviso da vez, com a prioridade queda > erro > vez > conexão."""
        estado = self.estado
        partes = []
        if estado is not None and estado.ausentes:
            nomes = [
                estado.assentos[assento] or f"assento {assento}"
                for assento in estado.ausentes
            ]
            partes.append(f"Mesa congelada — caído: {', '.join(nomes)}")
        if self.aviso_erro:
            partes.append(self.aviso_erro)
        if estado is not None and estado.vez is not None and not estado.encerrado:
            if estado.vez == self.meu_assento:
                partes.append("Sua vez")
            else:
                partes.append(f"Vez de {estado.assentos[estado.vez] or '?'}")
        if not partes:
            return "Conectando..." if estado is None else ""
        return " | ".join(partes)

    def desenhar_aviso(self) -> None:
        """Redesenha o painel de aviso a partir do estado corrente."""
        self.query_one("#aviso", Static).update(self.texto_aviso())


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

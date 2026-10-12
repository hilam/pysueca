"""Testes do cliente TUI — tela, teclas e linha de comando (sprint 06)."""

from __future__ import annotations

import asyncio
import socket
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Awaitable, Callable

import pytest
from textual.widgets import Static

from pysueca.carta import Carta
from pysueca.main import RespostaScreen, SuecaApp, desenhar_carta
from pysueca.protocolo import (
    Entrar,
    Erro,
    Estado,
    Jogar,
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
        await aguardar(pilot, lambda: "fora_de_hora" in painel(app, "#aviso"))
        assert "fora_de_hora" in painel(app, "#aviso")

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
        await falso.enviar(Estado(assentos=["Ana", "Bia", None, None], mao=[]))
        await aguardar(pilot, lambda: "2 de 4" in painel(app, "#assentos"))
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

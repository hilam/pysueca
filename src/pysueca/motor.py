"""Regras de uma mão de Sueca: a vaza e a mão."""

from __future__ import annotations

import enum
import random
from dataclasses import dataclass, field

from pysueca.baralho import Baralho
from pysueca.carta import Carta, Naipe


class ErroJogada(enum.Enum):
    """Motivos de recusa de uma jogada; devolvidos em vez de exceção."""

    FORA_DA_VEZ = "fora_da_vez"
    CARTA_FORA_DA_MAO = "carta_fora_da_mao"
    NAO_SEGUIU_NAIPE = "nao_seguiu_naipe"


def jogada_legal(mao: list[Carta], naipe_puxado: Naipe, carta: Carta) -> bool:
    """A carta segue o naipe puxado quando a mão tem alguma; senão, qualquer uma."""
    if carta.naipe is naipe_puxado:
        return True
    return all(outra.naipe is not naipe_puxado for outra in mao)


@dataclass
class Vaza:
    """As cartas jogadas numa vaza e quem leva."""

    naipe_puxado: Naipe
    trunfo: Naipe
    jogadas: list[tuple[int, Carta]] = field(default_factory=list)

    @property
    def vencedor(self) -> int:
        assento, carta = self.jogadas[0]
        for outro_assento, outra in self.jogadas[1:]:
            if outra.vence(carta, self.naipe_puxado, self.trunfo):
                assento, carta = outro_assento, outra
        return assento


class Resultado(enum.Enum):
    """O resultado de uma mão pelos limites de pontos do README."""

    EMPATE = "empate"
    NORMAL = "normal"
    QUILO = "quilo"
    BANDEIRA = "bandeira"

    @classmethod
    def de_pontos(cls, dupla_0_2: int, dupla_1_3: int) -> Resultado:
        melhor = max(dupla_0_2, dupla_1_3)
        if melhor == 60:
            return cls.EMPATE
        if melhor == 120:
            return cls.BANDEIRA
        if melhor >= 91:
            return cls.QUILO
        return cls.NORMAL

    @property
    def partidas(self) -> int:
        """Quantas partidas a mão vale para a dupla vencedora."""
        return {
            Resultado.EMPATE: 0,
            Resultado.NORMAL: 1,
            Resultado.QUILO: 2,
            Resultado.BANDEIRA: 4,
        }[self]


class Mao:
    """Uma mão completa: preparação, dez vazas e a pontuação."""

    def __init__(self, embaralhador: int, rng: random.Random | None = None) -> None:
        self.embaralhador = embaralhador
        self.rng = rng if rng is not None else random.Random()
        self.maos: list[list[Carta]] = [[], [], [], []]
        self.vez = embaralhador
        self.vaza: Vaza | None = None
        self.vazas: list[Vaza] = []

    def preparar(self, cima: bool = True) -> None:
        baralho = Baralho(self.rng)
        baralho.embaralhar()
        cartas = baralho.cartas
        self.carta_trunfo = cartas.pop(0 if cima else -1)
        self.trunfo = self.carta_trunfo.naipe
        dador = (self.embaralhador + 3) % 4
        self.maos = [[], [], [], []]
        for i, carta in enumerate(cartas):
            self.maos[(dador + 1 + i) % 4].append(carta)
        self.maos[dador].append(self.carta_trunfo)
        self.vez = self.embaralhador
        self.vaza = None
        self.vazas = []

    def jogar(self, assento: int, carta: Carta) -> ErroJogada | None:
        erro = self._validar(assento, carta)
        if erro is not None:
            return erro
        self.maos[assento].remove(carta)
        if self.vaza is None:
            self.vaza = Vaza(carta.naipe, self.trunfo)
        self.vaza.jogadas.append((assento, carta))
        if len(self.vaza.jogadas) == 4:
            self.vazas.append(self.vaza)
            self.vez = self.vaza.vencedor
            self.vaza = None
        else:
            self.vez = (assento + 1) % 4
        return None

    def _validar(self, assento: int, carta: Carta) -> ErroJogada | None:
        """O erro da jogada, ou `None`; não toca no estado."""
        if assento != self.vez:
            return ErroJogada.FORA_DA_VEZ
        if carta not in self.maos[assento]:
            return ErroJogada.CARTA_FORA_DA_MAO
        if self.vaza is not None and not jogada_legal(
            self.maos[assento], self.vaza.naipe_puxado, carta
        ):
            return ErroJogada.NAO_SEGUIU_NAIPE
        return None

    @property
    def pontos(self) -> tuple[int, int]:
        totais = [0, 0]
        for vaza in self.vazas:
            totais[vaza.vencedor % 2] += sum(carta.pontos for _, carta in vaza.jogadas)
        return (totais[0], totais[1])

    @property
    def resultado(self) -> Resultado:
        return Resultado.de_pontos(*self.pontos)


class Jogo:
    """A mesa: a mão corrente, o placar por dupla e o fim do jogo."""

    def __init__(self, rng: random.Random | None = None, embaralhador: int = 0) -> None:
        self.rng = rng if rng is not None else random.Random()
        self.embaralhador = embaralhador
        self.partidas = [0, 0]
        self.mao = Mao(embaralhador, self.rng)

    def preparar(self, cima: bool = True) -> None:
        self.mao.preparar(cima)

    def jogar(self, assento: int, carta: Carta) -> ErroJogada | None:
        return self.mao.jogar(assento, carta)

    def encerrar_mao(self) -> Resultado:
        """Soma a mão ao placar da dupla vencedora e abre a mão seguinte."""
        resultado = self.mao.resultado
        if resultado is not Resultado.EMPATE:
            dupla = 0 if self.mao.pontos[0] > self.mao.pontos[1] else 1
            self.partidas[dupla] += resultado.partidas
        self.embaralhador = (self.embaralhador + 1) % 4
        self.mao = Mao(self.embaralhador, self.rng)
        return resultado

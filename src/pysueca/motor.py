"""Regras de uma mão de Sueca: a vaza e a mão."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from pysueca.baralho import Baralho
from pysueca.carta import Carta, Naipe


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


class Mao:
    """Uma mão completa: preparação, dez vazas e a pontuação."""

    def __init__(self, embaralhador: int, rng: random.Random | None = None) -> None:
        self.embaralhador = embaralhador
        self.rng = rng if rng is not None else random.Random()
        self.maos: list[list[Carta]] = [[], [], [], []]

    def preparar(self, cima: bool = True) -> None:
        baralho = Baralho(self.rng)
        baralho.embaralhar()
        for i, carta in enumerate(baralho.cartas):
            self.maos[i % 4].append(carta)

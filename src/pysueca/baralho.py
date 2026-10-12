"""As 40 cartas de Sueca e o embaralhamento com RNG injetado."""

from __future__ import annotations

import random

from pysueca.carta import Carta, Naipe, Valor


class Baralho:
    """As 40 cartas de um jogo de quatro pessoas, embaralháveis."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng if rng is not None else random.Random()
        self.cartas = [Carta(naipe, valor) for naipe in Naipe for valor in Valor]

    def embaralhar(self) -> None:
        self.rng.shuffle(self.cartas)

"""Regras de uma mão de Sueca: a vaza e a mão."""

from __future__ import annotations

from dataclasses import dataclass, field

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

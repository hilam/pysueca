"""Testes do motor puro: vaza e mão (sprint 02)."""

from pysueca.carta import Carta, Naipe, Valor
from pysueca.motor import Vaza


def test_trunfo_vence_o_naipe_puxado() -> None:
    vaza = Vaza(
        naipe_puxado=Naipe.COPAS,
        trunfo=Naipe.OUROS,
        jogadas=[(0, Carta(Naipe.COPAS, Valor.AS)), (1, Carta(Naipe.OUROS, Valor.DOIS))],
    )
    assert vaza.vencedor == 1

"""Testes do motor puro: carta e baralho (sprint 01)."""

from pysueca.baralho import Baralho
from pysueca.carta import Carta, Naipe, Valor


def test_carta_formada_por_naipe_e_valor() -> None:
    carta = Carta(Naipe.COPAS, Valor.SETE)
    assert carta.naipe is Naipe.COPAS
    assert carta.valor is Valor.SETE


def test_baralho_tem_40_cartas_distintas() -> None:
    baralho = Baralho()
    assert len(baralho.cartas) == 40
    assert len(set(baralho.cartas)) == 40

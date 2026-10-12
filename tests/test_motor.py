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


def test_entre_trunfos_vence_a_maior() -> None:
    vaza = Vaza(
        naipe_puxado=Naipe.COPAS,
        trunfo=Naipe.OUROS,
        jogadas=[(0, Carta(Naipe.OUROS, Valor.REI)), (1, Carta(Naipe.OUROS, Valor.SETE))],
    )
    assert vaza.vencedor == 1


def test_maior_forca_do_naipe_puxado_vence_os_descartes() -> None:
    vaza = Vaza(
        naipe_puxado=Naipe.COPAS,
        trunfo=Naipe.OUROS,
        jogadas=[
            (0, Carta(Naipe.COPAS, Valor.AS)),
            (1, Carta(Naipe.COPAS, Valor.REI)),
            (2, Carta(Naipe.PAUS, Valor.AS)),
            (3, Carta(Naipe.ESPADAS, Valor.DOIS)),
        ],
    )
    assert vaza.vencedor == 0

"""Testes do motor puro: vaza e mão (sprint 02)."""

import random

from pysueca.baralho import Baralho
from pysueca.carta import Carta, Naipe, Valor
from pysueca.motor import Mao, Vaza


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


def test_preparacao_distribui_10_cartas_por_assento() -> None:
    mao = Mao(0, random.Random(42))
    mao.preparar(cima=True)

    assert [len(m) for m in mao.maos] == [10, 10, 10, 10]
    todas = [carta for m in mao.maos for carta in m]
    assert len(set(todas)) == 40
    assert set(todas) == set(Baralho().cartas)


def test_carta_do_trunfo_fica_com_o_dador() -> None:
    mao = Mao(0, random.Random(42))
    mao.preparar(cima=True)

    assert mao.carta_trunfo in mao.maos[3]
    assert mao.trunfo is mao.carta_trunfo.naipe


def test_cima_ou_baixo_escolhe_a_ponta_do_baralho() -> None:
    referencia = Baralho(random.Random(42))
    referencia.embaralhar()

    cima = Mao(0, random.Random(42))
    cima.preparar(cima=True)
    baixo = Mao(0, random.Random(42))
    baixo.preparar(cima=False)

    assert cima.carta_trunfo == referencia.cartas[0]
    assert baixo.carta_trunfo == referencia.cartas[-1]

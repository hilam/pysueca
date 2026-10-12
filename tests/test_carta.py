"""Testes do motor puro: carta e baralho (sprint 01)."""

import random

import pytest

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


def test_cada_naipe_tem_os_10_valores() -> None:
    baralho = Baralho()
    for naipe in Naipe:
        valores = {carta.valor for carta in baralho.cartas if carta.naipe is naipe}
        assert valores == set(Valor)


def test_pontos_dos_valores_com_ponto() -> None:
    assert Carta(Naipe.PAUS, Valor.AS).pontos == 11
    assert Carta(Naipe.PAUS, Valor.SETE).pontos == 10
    assert Carta(Naipe.PAUS, Valor.REI).pontos == 4
    assert Carta(Naipe.PAUS, Valor.VALETE).pontos == 3
    assert Carta(Naipe.PAUS, Valor.DAMA).pontos == 2


def test_soma_dos_pontos_do_baralho_e_120() -> None:
    baralho = Baralho()
    assert sum(carta.pontos for carta in baralho.cartas) == 120


def test_as_mais_forte_que_sete() -> None:
    as_de_copas = Carta(Naipe.COPAS, Valor.AS)
    sete_de_copas = Carta(Naipe.COPAS, Valor.SETE)
    assert as_de_copas.forca > sete_de_copas.forca


def test_texto_ida_e_volta_preserva_naipe_e_valor() -> None:
    carta = Carta.de_texto("7H")
    assert carta.naipe is Naipe.COPAS
    assert carta.valor is Valor.SETE
    assert carta.texto() == "7H"


def test_as_de_trunfo_vence_qualquer_carta() -> None:
    as_de_trunfo = Carta(Naipe.COPAS, Valor.AS)
    outras = [carta for carta in Baralho().cartas if carta != as_de_trunfo]
    assert len(outras) == 39
    for naipe_puxado in Naipe:
        for outra in outras:
            assert as_de_trunfo.vence(outra, naipe_puxado, Naipe.COPAS)


def test_entre_trunfos_vence_a_maior() -> None:
    sete_de_trunfo = Carta(Naipe.COPAS, Valor.SETE)
    rei_de_trunfo = Carta(Naipe.COPAS, Valor.REI)
    assert sete_de_trunfo.vence(rei_de_trunfo, Naipe.COPAS, Naipe.COPAS)
    assert not rei_de_trunfo.vence(sete_de_trunfo, Naipe.COPAS, Naipe.COPAS)


def test_naipe_puxado_vence_o_descarte_de_forca_maior() -> None:
    rei_de_copas = Carta(Naipe.COPAS, Valor.REI)
    as_de_paus = Carta(Naipe.PAUS, Valor.AS)
    assert rei_de_copas.vence(as_de_paus, Naipe.COPAS, Naipe.OUROS)
    assert not as_de_paus.vence(rei_de_copas, Naipe.COPAS, Naipe.OUROS)


def test_trunfo_vence_o_naipe_puxado() -> None:
    dois_de_trunfo = Carta(Naipe.OUROS, Valor.DOIS)
    as_de_copas = Carta(Naipe.COPAS, Valor.AS)
    assert dois_de_trunfo.vence(as_de_copas, Naipe.COPAS, Naipe.OUROS)
    assert not as_de_copas.vence(dois_de_trunfo, Naipe.COPAS, Naipe.OUROS)


def test_mesma_seed_mesma_ordem() -> None:
    um = Baralho(random.Random(42))
    dois = Baralho(random.Random(42))
    um.embaralhar()
    dois.embaralhar()
    assert um.cartas == dois.cartas


def test_embaralhar_preserva_as_40_cartas() -> None:
    baralho = Baralho(random.Random(7))
    antes = set(baralho.cartas)
    baralho.embaralhar()
    assert len(baralho.cartas) == 40
    assert len(set(baralho.cartas)) == 40
    assert set(baralho.cartas) == antes


def test_valor_sem_ponto_vale_zero() -> None:
    for valor in (Valor.SEIS, Valor.CINCO, Valor.QUATRO, Valor.TRES, Valor.DOIS):
        assert Carta(Naipe.COPAS, valor).pontos == 0

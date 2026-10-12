"""Testes do motor puro: vaza e mão (sprint 02)."""

import random

from pysueca.baralho import Baralho
from pysueca.carta import Carta, Naipe, Valor
from pysueca.motor import ErroJogada, Mao, Resultado, Vaza


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


def test_ao_puxar_qualquer_carta_e_aceita() -> None:
    mao = Mao(0, random.Random(1))
    mao.preparar()

    carta = mao.maos[0][0]
    assert mao.vez == 0
    assert mao.jogar(0, carta) is None

    assert mao.vaza is not None
    assert mao.vaza.naipe_puxado is carta.naipe
    assert carta not in mao.maos[0]
    assert mao.vez == 1


def test_assento_com_o_naipe_puxado_e_obrigado_a_joga_lo() -> None:
    mao = Mao(0, random.Random(1))
    mao.preparar()

    copas = Carta(Naipe.COPAS, Valor.AS)
    paus = Carta(Naipe.PAUS, Valor.SETE)
    mao.maos[0] = [copas, paus]
    mao.vez = 0
    mao.vaza = Vaza(Naipe.COPAS, mao.trunfo, [(1, Carta(Naipe.COPAS, Valor.REI))])

    assert mao.jogar(0, paus) is ErroJogada.NAO_SEGUIU_NAIPE
    assert paus in mao.maos[0]


def test_sem_o_naipe_puxado_pode_jogar_qualquer_carta() -> None:
    mao = Mao(0, random.Random(1))
    mao.preparar()

    trunfo = Carta(Naipe.OUROS, Valor.DOIS)
    descarte = Carta(Naipe.PAUS, Valor.AS)
    mao.maos[0] = [trunfo, descarte]
    mao.vez = 0
    mao.vaza = Vaza(Naipe.COPAS, Naipe.OUROS, [(1, Carta(Naipe.COPAS, Valor.REI))])

    assert mao.jogar(0, trunfo) is None
    assert mao.vaza.jogadas[-1] == (0, trunfo)


def test_quem_levou_a_vaza_puxa_a_seguinte() -> None:
    mao = Mao(0, random.Random(1))
    mao.preparar()

    rei_de_copas = Carta(Naipe.COPAS, Valor.REI)
    as_de_copas = Carta(Naipe.COPAS, Valor.AS)
    as_de_paus = Carta(Naipe.PAUS, Valor.AS)
    as_de_espadas = Carta(Naipe.ESPADAS, Valor.AS)
    mao.maos[0] = [rei_de_copas]
    mao.maos[1] = [as_de_copas]
    mao.maos[2] = [as_de_paus]
    mao.maos[3] = [as_de_espadas]
    mao.trunfo = Naipe.OUROS
    mao.vez = 0

    assert mao.jogar(0, rei_de_copas) is None
    assert mao.jogar(1, as_de_copas) is None
    assert mao.jogar(2, as_de_paus) is None
    assert mao.jogar(3, as_de_espadas) is None

    assert len(mao.vazas) == 1
    assert mao.vez == 1


def test_mao_completa_sao_10_vazas_e_esvazia_as_maos() -> None:
    mao = Mao(0, random.Random(7))
    mao.preparar()
    rng = random.Random(0)

    while any(mao.maos):
        assento = mao.vez
        legais = mao.maos[assento]
        if mao.vaza is not None:
            do_naipe = [c for c in legais if c.naipe is mao.vaza.naipe_puxado]
            if do_naipe:
                legais = do_naipe
        assert mao.jogar(assento, rng.choice(legais)) is None

    assert len(mao.vazas) == 10
    assert all(not maos for maos in mao.maos)


def test_pontuacao_da_mao_jogada() -> None:
    mao = Mao(0, random.Random(7))
    mao.preparar()
    rng = random.Random(0)

    while any(mao.maos):
        assento = mao.vez
        legais = mao.maos[assento]
        if mao.vaza is not None:
            do_naipe = [c for c in legais if c.naipe is mao.vaza.naipe_puxado]
            if do_naipe:
                legais = do_naipe
        assert mao.jogar(assento, rng.choice(legais)) is None

    assert mao.pontos == (88, 32)
    assert sum(mao.pontos) == 120
    assert mao.resultado is Resultado.de_pontos(88, 32)
    assert mao.resultado is Resultado.NORMAL


def test_resultado_pelos_limites_do_readme() -> None:
    assert Resultado.de_pontos(60, 60) is Resultado.EMPATE
    assert Resultado.de_pontos(61, 59) is Resultado.NORMAL
    assert Resultado.de_pontos(90, 30) is Resultado.NORMAL
    assert Resultado.de_pontos(91, 29) is Resultado.QUILO
    assert Resultado.de_pontos(119, 1) is Resultado.QUILO
    assert Resultado.de_pontos(120, 0) is Resultado.BANDEIRA


def test_jogada_fora_da_vez_devolve_erro() -> None:
    mao = Mao(0, random.Random(1))
    mao.preparar()
    assert mao.vez == 0

    carta = mao.maos[2][0]
    assert mao.jogar(2, carta) is ErroJogada.FORA_DA_VEZ
    assert carta in mao.maos[2]

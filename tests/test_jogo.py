"""Testes do jogo: placar por dupla, rotação de papéis e fim da mesa (sprint 03)."""

import random

from pysueca.motor import ErroJogada, Jogo, Mao, Resultado


class _MaoDePlacar(Mao):
    """Uma `Mao` com placar fixo, só para os cenários de placar do `Jogo`."""

    def __init__(self, pontos: tuple[int, int]) -> None:
        super().__init__(0)
        self._pontos = pontos

    @property
    def pontos(self) -> tuple[int, int]:
        return self._pontos


def _jogar_mao_inteira(jogo: Jogo, rng: random.Random) -> None:
    while any(jogo.mao.maos):
        assento = jogo.mao.vez
        legais = jogo.mao.maos[assento]
        if jogo.mao.vaza is not None:
            do_naipe = [c for c in legais if c.naipe is jogo.mao.vaza.naipe_puxado]
            if do_naipe:
                legais = do_naipe
        assert jogo.jogar(assento, rng.choice(legais)) is None


def test_embaralhador_puxa_a_primeira_vaza() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)

    assert jogo.mao.vez == 0
    assert jogo.jogar(0, jogo.mao.maos[0][0]) is None
    assert jogo.mao.vez == 1


def test_jogo_jogar_devolve_o_erro_do_motor() -> None:
    jogo = Jogo(random.Random(1), embaralhador=0)
    jogo.preparar()
    assert jogo.mao.vez == 0

    carta = jogo.mao.maos[2][0]
    assert jogo.jogar(2, carta) is ErroJogada.FORA_DA_VEZ
    assert carta in jogo.mao.maos[2]
    assert jogo.mao.vez == 0


def test_partidas_que_a_mao_vale() -> None:
    assert Resultado.EMPATE.partidas == 0
    assert Resultado.NORMAL.partidas == 1
    assert Resultado.QUILO.partidas == 2
    assert Resultado.BANDEIRA.partidas == 4


def test_mao_normal_soma_uma_partida_a_dupla_vencedora() -> None:
    jogo = Jogo(random.Random(1), embaralhador=0)
    jogo.mao = _MaoDePlacar((70, 50))

    assert jogo.encerrar_mao() is Resultado.NORMAL
    assert jogo.partidas == [1, 0]


def test_quilo_soma_duas_partidas_a_dupla_1() -> None:
    jogo = Jogo(random.Random(1), embaralhador=0)
    jogo.mao = _MaoDePlacar((29, 91))

    assert jogo.encerrar_mao() is Resultado.QUILO
    assert jogo.partidas == [0, 2]


def test_empate_nao_da_partida_a_ninguem() -> None:
    jogo = Jogo(random.Random(1), embaralhador=0)
    jogo.mao = _MaoDePlacar((60, 60))

    assert jogo.encerrar_mao() is Resultado.EMPATE
    assert jogo.partidas == [0, 0]
    assert jogo.embaralhador == 1


def test_papeis_andam_um_assento_por_mao() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)
    _jogar_mao_inteira(jogo, random.Random(0))
    assert len(jogo.mao.vazas) == 10

    jogo.encerrar_mao()
    assert jogo.embaralhador == 1
    assert jogo.mao.embaralhador == 1

    jogo.preparar(cima=True)
    assert jogo.mao.vez == 1
    assert jogo.mao.carta_trunfo in jogo.mao.maos[0]  # dador = (1 + 3) % 4

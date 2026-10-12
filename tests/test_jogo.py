"""Testes do jogo: placar por dupla, rotação de papéis e fim da mesa (sprint 03)."""

import random

from pysueca.motor import Jogo


def test_embaralhador_puxa_a_primeira_vaza() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)

    assert jogo.mao.vez == 0
    assert jogo.jogar(0, jogo.mao.maos[0][0]) is None
    assert jogo.mao.vez == 1

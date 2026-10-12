"""Testes do protocolo de fio — mensagens, validação e snapshot (sprint 04)."""

import json

from pysueca.carta import Carta, Naipe, Valor
from pysueca.protocolo import Entrar, Jogar, desserializar, serializar


def test_entrar_faz_ida_e_volta() -> None:
    assert desserializar(serializar(Entrar("Ana"))) == Entrar("Ana")


def test_jogar_faz_ida_e_volta() -> None:
    linha = serializar(Jogar(Carta(Naipe.COPAS, Valor.SETE)))

    assert json.loads(linha)["carta"] == "7H"
    assert desserializar(linha) == Jogar(Carta(Naipe.COPAS, Valor.SETE))

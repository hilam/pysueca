"""Testes do protocolo de fio — mensagens, validação e snapshot (sprint 04)."""

from pysueca.protocolo import Entrar, desserializar, serializar


def test_entrar_faz_ida_e_volta() -> None:
    assert desserializar(serializar(Entrar("Ana"))) == Entrar("Ana")

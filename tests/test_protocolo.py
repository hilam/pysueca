"""Testes do protocolo de fio — mensagens, validação e snapshot (sprint 04)."""

import json

from pysueca.carta import Carta, Naipe, Valor
from pysueca.protocolo import Entrar, Erro, Jogar, Responder, desserializar, serializar


def test_entrar_faz_ida_e_volta() -> None:
    assert desserializar(serializar(Entrar("Ana"))) == Entrar("Ana")


def test_jogar_faz_ida_e_volta() -> None:
    linha = serializar(Jogar(Carta(Naipe.COPAS, Valor.SETE)))

    assert json.loads(linha)["carta"] == "7H"
    assert desserializar(linha) == Jogar(Carta(Naipe.COPAS, Valor.SETE))


def test_responder_faz_ida_e_volta() -> None:
    for cima in (True, False):
        linha = serializar(Responder(cima))

        assert json.loads(linha)["cima"] is cima
        assert desserializar(linha) == Responder(cima)


def test_linha_malformada_vira_erro() -> None:
    for linha in (b"{", b"nao e json", b"[1, 2]"):
        assert desserializar(linha) == Erro("json_invalido")


def test_tipo_desconhecido_vira_erro() -> None:
    assert desserializar(b'{"tipo": "assobiar"}') == Erro("tipo_desconhecido")


def test_campo_faltando_vira_erro() -> None:
    for linha in (b'{"tipo": "jogar"}', b'{"tipo": "entrar"}', b'{"tipo": "responder"}'):
        assert desserializar(linha) == Erro("campo_faltando")


def test_nome_e_normalizado() -> None:
    assert desserializar(b'{"tipo": "entrar", "nome": "  Ana  "}') == Entrar("Ana")

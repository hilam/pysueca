"""Testes do protocolo de fio — mensagens, validação e snapshot (sprint 04)."""

import json
import random

import pytest

from pysueca.carta import Carta, Naipe, Valor
from pysueca.motor import ErroJogada, Jogo, Vaza
from pysueca.protocolo import (
    TETO_LINHA,
    Entrar,
    Erro,
    Estado,
    Jogar,
    LinhaLonga,
    Responder,
    desserializar,
    erro_de_jogada,
    estado,
    serializar,
)


def _linha_de_tamanho(tamanho: int) -> bytes:
    """Um `entrar` válido de exatamente `tamanho` bytes, com espaço de enchimento."""
    corpo = b'{"tipo": "entrar", "nome": "Ana"}'
    return corpo + b" " * (tamanho - 1 - len(corpo)) + b"\n"


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
    for linha in (
        b'{"tipo": "jogar"}',
        b'{"tipo": "entrar"}',
        b'{"tipo": "responder"}',
    ):
        assert desserializar(linha) == Erro("campo_faltando")


def test_nome_e_normalizado() -> None:
    assert desserializar(b'{"tipo": "entrar", "nome": "  Ana  "}') == Entrar("Ana")


def test_nome_invalido_vira_erro() -> None:
    for nome in ("   ", "x" * 21):
        assert desserializar(serializar(Entrar(nome))) == Erro("nome_invalido")


def test_campo_extra_vira_erro() -> None:
    assert desserializar(b'{"tipo": "jogar", "carta": "7H", "cor": "azul"}') == Erro(
        "campo_extra"
    )


def test_campo_com_tipo_errado_vira_erro() -> None:
    assert desserializar(b'{"tipo": "jogar", "carta": 7}') == Erro("campo_invalido")


def test_linha_acima_do_teto_e_fatal() -> None:
    with pytest.raises(LinhaLonga):
        desserializar(_linha_de_tamanho(TETO_LINHA + 1))


def test_linha_no_limite_e_aceita() -> None:
    assert desserializar(_linha_de_tamanho(TETO_LINHA)) == Entrar("Ana")


def test_nenhum_outro_erro_e_fatal() -> None:
    for linha in (b"{", b'{"tipo": "assobiar"}', b'{"tipo": "jogar"}'):
        assert isinstance(desserializar(linha), Erro)


def test_snapshot_traz_a_propria_mao() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)

    snap = estado(jogo, ["Ana", "Bia", "Caio", "Dora"], assento=2)

    assert snap.mao == [carta.texto() for carta in jogo.mao.maos[2]]


def test_estado_faz_ida_e_volta() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)
    snap = estado(jogo, ["Ana", "Bia", "Caio", "Dora"], assento=2)

    assert desserializar(serializar(snap)) == snap


def test_erro_faz_ida_e_volta() -> None:
    erro = erro_de_jogada(ErroJogada.FORA_DA_VEZ)

    assert desserializar(serializar(erro)) == Erro("fora_da_vez")


def test_snapshot_traz_so_a_contagem_das_outras_maos() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)
    trunfo = jogo.mao.carta_trunfo

    snap = estado(jogo, ["Ana", "Bia", "Caio", "Dora"], assento=2)
    linha = serializar(snap)

    assert snap.contagens == [10, 10, 10, 10]
    for outro in (0, 1, 3):
        for carta in jogo.mao.maos[outro]:
            if carta == trunfo:
                continue  # a carta do trunfo é pública: virada na mesa
            assert f'"{carta.texto()}"'.encode() not in linha


def test_snapshot_reflete_a_mesa() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)
    jogo.partidas = [2, 0]
    carta = jogo.mao.maos[0][0]
    jogo.jogar(0, carta)

    snap = estado(jogo, ["Ana", "Bia", "Caio", "Dora"], assento=2)

    assert snap.trunfo == jogo.mao.trunfo.value
    assert snap.carta_trunfo == jogo.mao.carta_trunfo.texto()
    assert snap.vez == 1
    assert snap.vaza == [(0, carta.texto())]
    assert snap.partidas == [2, 0]
    assert snap.encerrado is False


def test_snapshot_diz_quem_deve_responder() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)

    pendente = estado(jogo, ["Ana", "Bia", "Caio", "Dora"], assento=2)
    assert pendente.respondente == 1

    jogo.preparar(cima=True)
    respondida = estado(jogo, ["Ana", "Bia", "Caio", "Dora"], assento=2)
    assert respondida.respondente is None


def test_jogada_fora_da_vez_vira_erro() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)

    erro = jogo.jogar(1, jogo.mao.maos[1][0])

    assert erro == ErroJogada.FORA_DA_VEZ
    assert erro_de_jogada(erro) == Erro("fora_da_vez")


def test_carta_fora_da_mao_vira_erro() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.preparar(cima=True)

    erro = jogo.jogar(0, jogo.mao.maos[1][0])

    assert erro == ErroJogada.CARTA_FORA_DA_MAO
    assert erro_de_jogada(erro) == Erro("carta_fora_da_mao")


def test_nao_seguir_o_naipe_vira_erro() -> None:
    jogo = Jogo(random.Random(7), embaralhador=0)
    jogo.mao.vaza = Vaza(naipe_puxado=Naipe.COPAS, trunfo=Naipe.OUROS)
    jogo.mao.vez = 0
    jogo.mao.maos[0] = [Carta(Naipe.COPAS, Valor.DOIS), Carta(Naipe.PAUS, Valor.AS)]

    erro = jogo.jogar(0, Carta(Naipe.PAUS, Valor.AS))

    assert erro == ErroJogada.NAO_SEGUIU_NAIPE
    assert erro_de_jogada(erro) == Erro("nao_seguiu_naipe")


def test_estado_carrega_os_assentos_ausentes() -> None:
    for ausentes in ([2], []):
        snap = Estado(
            assentos=["Ana", "Bia", "Caio", "Dora"], mao=[], ausentes=ausentes
        )
        linha = serializar(snap)

        assert json.loads(linha)["ausentes"] == ausentes
        assert desserializar(linha) == snap


def test_ausentes_com_tipo_errado_vira_erro() -> None:
    linha = (
        b'{"tipo": "estado", "assentos": [], "mao": [], "contagens": [],'
        b' "trunfo": null, "carta_trunfo": null, "vez": null, "respondente": null,'
        b' "vaza": [], "partidas": [], "encerrado": false, "vencedor": null,'
        b' "ausentes": "todos"}'
    )

    assert desserializar(linha) == Erro("campo_invalido")

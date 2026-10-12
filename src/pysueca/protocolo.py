"""Formato de fio: mensagens do jogo em uma linha JSON (sprint 04)."""

from __future__ import annotations

import json
from dataclasses import dataclass

from pysueca.carta import Carta


@dataclass(frozen=True)
class Entrar:
    """Intenção do cliente: sentar no jogo com um nome."""

    nome: str


@dataclass(frozen=True)
class Jogar:
    """Intenção do cliente: jogar uma carta da própria mão."""

    carta: Carta


@dataclass(frozen=True)
class Responder:
    """Intenção do cliente: se a carta do trunfo é a de cima ou a de baixo."""

    cima: bool


def serializar(mensagem: Entrar | Jogar | Responder) -> bytes:
    """A linha JSON da mensagem, terminada em `\\n`."""
    if isinstance(mensagem, Entrar):
        dados = {"tipo": "entrar", "nome": mensagem.nome}
    elif isinstance(mensagem, Jogar):
        dados = {"tipo": "jogar", "carta": mensagem.carta.texto()}
    else:
        dados = {"tipo": "responder", "cima": mensagem.cima}
    return (json.dumps(dados) + "\n").encode()


def desserializar(linha: bytes) -> Entrar | Jogar | Responder:
    """A mensagem da linha lida do fio."""
    dados = json.loads(linha.decode())
    if dados["tipo"] == "jogar":
        return Jogar(Carta.de_texto(dados["carta"]))
    if dados["tipo"] == "responder":
        return Responder(dados["cima"])
    return Entrar(dados["nome"])

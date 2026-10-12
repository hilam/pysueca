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


@dataclass(frozen=True)
class Erro:
    """Recusa recuperável do protocolo: a mesa segue, o cliente recebe o motivo."""

    motivo: str


def serializar(mensagem: Entrar | Jogar | Responder) -> bytes:
    """A linha JSON da mensagem, terminada em `\\n`."""
    if isinstance(mensagem, Entrar):
        dados = {"tipo": "entrar", "nome": mensagem.nome}
    elif isinstance(mensagem, Jogar):
        dados = {"tipo": "jogar", "carta": mensagem.carta.texto()}
    else:
        dados = {"tipo": "responder", "cima": mensagem.cima}
    return (json.dumps(dados) + "\n").encode()


_CAMPOS: dict[str, dict[str, type | tuple[type, ...]]] = {
    "entrar": {"nome": str},
    "jogar": {"carta": str},
    "responder": {"cima": bool},
}


def _validar(tipo: str, dados: dict) -> str | None:
    """O motivo da recusa do corpo da mensagem, ou `None` se a forma está correta."""
    esperados = _CAMPOS[tipo]
    if set(dados) - {"tipo"} - set(esperados):
        return "campo_extra"
    if not {"tipo", *esperados} <= set(dados):
        return "campo_faltando"
    for campo, tipo_esperado in esperados.items():
        if not isinstance(dados[campo], tipo_esperado):
            return "campo_faltando"
    return None


def desserializar(linha: bytes) -> Entrar | Jogar | Responder | Erro:
    """A mensagem da linha lida do fio, ou o `Erro` recuperável."""
    try:
        dados = json.loads(linha.decode())
    except (UnicodeDecodeError, json.JSONDecodeError):
        return Erro("json_invalido")
    if not isinstance(dados, dict):
        return Erro("json_invalido")
    tipo = dados.get("tipo")
    if not isinstance(tipo, str) or tipo not in _CAMPOS:
        return Erro("tipo_desconhecido")
    motivo = _validar(tipo, dados)
    if motivo is not None:
        return Erro(motivo)
    if tipo == "entrar":
        nome = dados["nome"].strip()
        if not 1 <= len(nome) <= 20:
            return Erro("nome_invalido")
        return Entrar(nome)
    if tipo == "jogar":
        return Jogar(Carta.de_texto(dados["carta"]))
    return Responder(dados["cima"])

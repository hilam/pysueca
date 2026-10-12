"""Formato de fio: mensagens do jogo em uma linha JSON (sprint 04)."""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Entrar:
    """Intenção do cliente: sentar no jogo com um nome."""

    nome: str


def serializar(mensagem: Entrar) -> bytes:
    """A linha JSON da mensagem, terminada em `\\n`."""
    return (json.dumps({"tipo": "entrar", "nome": mensagem.nome}) + "\n").encode()


def desserializar(linha: bytes) -> Entrar:
    """A mensagem da linha lida do fio."""
    dados = json.loads(linha.decode())
    return Entrar(dados["nome"])

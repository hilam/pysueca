"""Formato de fio: mensagens do jogo em uma linha JSON (sprint 04)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from pysueca.carta import Carta
from pysueca.motor import ErroJogada, Jogo

TETO_LINHA = 4096


class LinhaLonga(Exception):
    """Linha acima do teto: único erro fatal, que fecha a conexão."""


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


@dataclass(frozen=True)
class Estado:
    """Snapshot completo por assento: a própria mão, as outras só como contagem."""

    assentos: list[str | None]
    mao: list[str]
    contagens: list[int] = field(default_factory=list)
    trunfo: str | None = None
    carta_trunfo: str | None = None
    vez: int | None = None
    respondente: int | None = None
    vaza: list[tuple[int, str]] = field(default_factory=list)
    partidas: list[int] = field(default_factory=list)
    encerrado: bool = False
    vencedor: int | None = None


type Mensagem = Entrar | Jogar | Responder | Estado | Erro


def estado(jogo: Jogo, nomes: list[str | None], assento: int) -> Estado:
    """O snapshot da mesa para um assento: a própria mão, as outras só como contagem."""
    mao = jogo.mao
    # a `Mao` só ganha `carta_trunfo` em `preparar()`; entre mãos, ela ainda não existe
    carta_trunfo = getattr(mao, "carta_trunfo", None)
    return Estado(
        assentos=list(nomes),
        mao=[carta.texto() for carta in mao.maos[assento]],
        contagens=[len(outra) for outra in mao.maos],
        trunfo=carta_trunfo.naipe.value if carta_trunfo is not None else None,
        carta_trunfo=carta_trunfo.texto() if carta_trunfo is not None else None,
        vez=mao.vez if carta_trunfo is not None else None,
        respondente=None if carta_trunfo is not None else (mao.embaralhador + 1) % 4,
        vaza=[(a, c.texto()) for a, c in (mao.vaza.jogadas if mao.vaza else [])],
        partidas=list(jogo.partidas),
        encerrado=jogo.encerrado,
        vencedor=jogo.vencedor,
    )


def erro_de_jogada(erro: ErroJogada) -> Erro:
    """Formata o erro de regra do motor como a mensagem `erro` de fio."""
    return Erro(erro.value)


def serializar(mensagem: Mensagem) -> bytes:
    """A linha JSON da mensagem, terminada em `\\n`."""
    return (json.dumps(_para_dados(mensagem)) + "\n").encode()


def _para_dados(mensagem: Mensagem) -> dict:
    """Os campos JSON da mensagem."""
    if isinstance(mensagem, Entrar):
        return {"tipo": "entrar", "nome": mensagem.nome}
    if isinstance(mensagem, Jogar):
        return {"tipo": "jogar", "carta": mensagem.carta.texto()}
    if isinstance(mensagem, Responder):
        return {"tipo": "responder", "cima": mensagem.cima}
    if isinstance(mensagem, Estado):
        return {
            "tipo": "estado",
            "assentos": mensagem.assentos,
            "mao": mensagem.mao,
            "contagens": mensagem.contagens,
            "trunfo": mensagem.trunfo,
            "carta_trunfo": mensagem.carta_trunfo,
            "vez": mensagem.vez,
            "respondente": mensagem.respondente,
            "vaza": [list(jogada) for jogada in mensagem.vaza],
            "partidas": mensagem.partidas,
            "encerrado": mensagem.encerrado,
            "vencedor": mensagem.vencedor,
        }
    return {"tipo": "erro", "motivo": mensagem.motivo}


_CAMPOS: dict[str, dict[str, type | tuple[type, ...]]] = {
    "entrar": {"nome": str},
    "jogar": {"carta": str},
    "responder": {"cima": bool},
    "erro": {"motivo": str},
    "estado": {
        "assentos": list,
        "mao": list,
        "contagens": list,
        "trunfo": (str, type(None)),
        "carta_trunfo": (str, type(None)),
        "vez": (int, type(None)),
        "respondente": (int, type(None)),
        "vaza": list,
        "partidas": list,
        "encerrado": bool,
        "vencedor": (int, type(None)),
    },
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


def desserializar(linha: bytes) -> Mensagem:
    """A mensagem da linha lida do fio, ou o `Erro` recuperável."""
    if len(linha) > TETO_LINHA:
        raise LinhaLonga(len(linha))
    try:
        dados = json.loads(linha.decode())
    except UnicodeDecodeError, json.JSONDecodeError:
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
    if tipo == "responder":
        return Responder(dados["cima"])
    if tipo == "estado":
        return Estado(
            assentos=dados["assentos"],
            mao=dados["mao"],
            contagens=dados["contagens"],
            trunfo=dados["trunfo"],
            carta_trunfo=dados["carta_trunfo"],
            vez=dados["vez"],
            respondente=dados["respondente"],
            vaza=[tuple(jogada) for jogada in dados["vaza"]],
            partidas=dados["partidas"],
            encerrado=dados["encerrado"],
            vencedor=dados["vencedor"],
        )
    return Erro(dados["motivo"])

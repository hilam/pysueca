"""Aritmética de uma carta de Sueca: naipe, valor, pontos, força e desempate."""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Self


class Naipe(enum.Enum):
    """Os quatro naipes. O valor é a letra do formato de fio (`"7H"`)."""

    PAUS = "C"
    COPAS = "H"
    ESPADAS = "S"
    OUROS = "D"


class Valor(enum.Enum):
    """A face da carta e sua aritmética: pontos de contagem e força de vaza."""

    _pontos: int
    _forca: int

    AS = ("A", 11, 9)
    SETE = ("7", 10, 8)
    REI = ("K", 4, 7)
    VALETE = ("J", 3, 6)
    DAMA = ("Q", 2, 5)
    SEIS = ("6", 0, 4)
    CINCO = ("5", 0, 3)
    QUATRO = ("4", 0, 2)
    TRES = ("3", 0, 1)
    DOIS = ("2", 0, 0)

    def __new__(cls, texto: str, pontos: int, forca: int) -> Self:
        obj = object.__new__(cls)
        obj._value_ = texto
        obj._pontos = pontos
        obj._forca = forca
        return obj

    @property
    def pontos(self) -> int:
        return self._pontos

    @property
    def forca(self) -> int:
        return self._forca


_NAIPE_POR_TEXTO = {naipe.value: naipe for naipe in Naipe}
_VALOR_POR_TEXTO = {valor.value: valor for valor in Valor}


@dataclass(frozen=True, slots=True)
class Carta:
    """Uma carta: par de `Naipe` e `Valor`."""

    naipe: Naipe
    valor: Valor

    @property
    def pontos(self) -> int:
        return self.valor.pontos

    @property
    def forca(self) -> int:
        return self.valor.forca

    def texto(self) -> str:
        return f"{self.valor.value}{self.naipe.value}"

    @classmethod
    def de_texto(cls, texto: str) -> Carta:
        if len(texto) != 2:
            raise ValueError(f"carta inválida: {texto!r}")
        try:
            valor = _VALOR_POR_TEXTO[texto[0]]
            naipe = _NAIPE_POR_TEXTO[texto[1]]
        except KeyError as erro:
            raise ValueError(f"carta inválida: {texto!r}") from erro
        return cls(naipe, valor)

    def vence(self, outra: Carta, naipe_puxado: Naipe, trunfo: Naipe) -> bool:
        """Trunfo > naipe puxado > descarte; dentro do naipe, vence a maior força."""

        def peso(carta: Carta) -> tuple[int, int]:
            if carta.naipe is trunfo:
                return (2, carta.forca)
            if carta.naipe is naipe_puxado:
                return (1, carta.forca)
            return (0, carta.forca)

        return peso(self) > peso(outra)

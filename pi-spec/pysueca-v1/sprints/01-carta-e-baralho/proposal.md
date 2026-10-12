# Proposal — Sprint 01 — Carta e baralho

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 01 — Carta e baralho
> **Depende de:** nenhuma

## Por que

O motor de regras não existe: não há como representar uma carta nem o baralho. Toda sprint seguinte (vaza/mão, jogo, protocolo, servidor, TUI) depende desta aritmética. É também o único lugar que pode saber a ordem de força `A > 7 > K > J > Q > 6 > 5 > 4 > 3 > 2`, que **não** é a ordem de pontos (`A=11, 7=10, K=4, J=3, Q=2`) — espalhar essa ordem por dois módulos é dívida garantida.

## O que muda

- **`src/pysueca/carta.py`** (novo) — `Naipe`, `Valor`, `Carta`; pontos por valor, força por valor, texto `"7H"` ida-e-volta e `vence(outra, naipe_puxado, trunfo)` para a vaza.
- **`src/pysueca/baralho.py`** (novo) — as 40 cartas e embaralhamento com `random.Random` injetado (default próprio, nunca o global).
- **`tests/test_carta.py`** (novo) — prova os pontos, a força, o texto e o trunfo.
- **`AGENTS.md`** (novo, raiz) — comandos `uv run`, mapa de arquivos, invariantes "motor puro e síncrono" e "só Textual", ponteiro para `docs/adr/` e `CONTEXT.md`. Incluir boas práticas de Python. Incluir Conventional Commits.

Nada de rede, `asyncio` ou Textual entra nesta sprint — `docs/adr/0004`.

## Capabilities

### New Capabilities
- `carta`: modelo e aritmética de uma carta — naipe, valor, pontos, força, texto `"7H"` e desempate de vaza com trunfo.
- `baralho`: as 40 cartas e o embaralhamento com RNG injetado.

### Modified Capabilities
- (nenhuma — projeto sem capabilities anteriores)

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/` | novos `carta.py` e `baralho.py`; `main.py` (57 linhas) intocado |
| `tests/` | diretório novo (não existe hoje) |
| `AGENTS.md` | arquivo novo na raiz |
| `pyproject.toml:6-8` | sem mudança; nenhuma dependência nova (`docs/adr/0004`) |
| `README.md`, `CONTEXT.md` | sem mudança — fontes canônicas de regra e vocabulário |
| `pyproject.toml:12` | entrypoint quebrado (`pysueca:src.pysueca.main`) permanece; fora do escopo desta sprint |

## Não objetivos

- Vaza, mão, jogo, placar (sprints 02–03).
- Protocolo, rede, UI.
- Distribuição "cima/baixo" (`README.md` item 5) — modelada só na sprint 02.
- Renderização `A♥` das cartas: o texto desta sprint é o formato de fio `"7H"`; o símbolo colorido é sprint 06 (`docs/adr/0004`).

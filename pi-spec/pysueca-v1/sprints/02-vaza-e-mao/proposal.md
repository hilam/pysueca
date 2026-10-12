# Proposal — Sprint 02 — Vaza e mão

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 02 — Vaza e mão
> **Depende de:** Sprint 01 — Carta e baralho (concluída)

## Por que

A aritmética de carta existe (`carta.py`, `baralho.py`), mas não há jogo: falta a **vaza** (a obrigação de seguir o naipe puxado e quem leva as quatro cartas) e a **mão** (embaralhar, puxar o trunfo, distribuir 10 cartas, 10 vazas e contar pontos). Sem esse motor, o protocolo (04), o servidor (05) e a TUI (06) não têm o que transportar. É também onde a regra "quem tem o naipe puxado é obrigado a jogá-lo" vira código — a validação que o servidor autoritativo precisa para rejeitar a jogada ilegal sem derrubar a mesa (ADR 0001).

## O que muda

- **`src/pysueca/motor.py`** (novo) — `Vaza` (naipe puxado, trunfo, jogadas, vencedor), `Mao` (máquina de estados `preparar → 10 vazas → pontuar`), `ErroJogada` e `Resultado`.
- **`tests/test_motor.py`** (novo) — vaza e mão sem rede, sem `asyncio` e sem Textual: obrigação de naipe, trunfo, vez, distribuição, pontos e os limites do README.

Nenhum arquivo da sprint 01 muda. Nada de rede, `asyncio` ou Textual entra aqui (`docs/adr/0004`).

## Capabilities

### New Capabilities
- `vaza`: a vaza — legalidade da jogada (seguir o naipe puxado, trunfar quando faltar) e quem leva as quatro cartas.
- `mao`: a mão completa — preparação (embaralhar, carta do trunfo, 10 cartas por assento), sequência de 10 vazas, erros de jogada ilegal e o resultado pelos limites do README.

### Modified Capabilities
- (nenhuma — `carta` e `baralho` são apenas consumidas)

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/motor.py` | arquivo novo — único módulo de regra da sprint |
| `src/pysueca/carta.py:85` | sem mudança; `Vaza.vencedor` reusa `Carta.vence(outra, naipe_puxado, trunfo)` |
| `src/pysueca/baralho.py:13,17` | sem mudança; `Mao` cria `Baralho(rng)` e chama `embaralhar()` |
| `tests/test_carta.py:56-83` | sem mudança; já prova o desempate par a par que a vaza agrega |
| `tests/test_motor.py` | arquivo novo |
| `src/pysueca/main.py:52` | intocado; `uv run mypy src` continua vermelho por `App.dark` (pré-existente, sprint 06) |
| `pyproject.toml:6-12` | sem mudança; nenhuma dependência nova (`docs/adr/0004`) e o entrypoint quebrado continua fora de escopo |

Consumidores futuros: `Jogo` (03) acumula `Mao.resultado` por dupla; `protocolo.py` (04) reusa `ErroJogada` para o `erro` de jogada ilegal; o servidor (05) chama `Mao.jogar`; a TUI (06) manda a resposta "cima ou baixo" que vira `Mao.preparar(cima=…)`.

## Não objetivos

- `Jogo`, placar acumulado e rotação de papéis (embaralhador/cortador/dador/respondente) — sprint 03.
- Formato de fio, snapshot e validação de rede — sprints 04–05.
- Modelar a ordem da distribuição "cima/baixo" além da ponta do baralho: `trunfo = cartas.pop(0|−1)`, o resto é sorteio (mitigação do risco declarada no PLANO).
- "Cortar o baralho" e a pergunta/resposta "cima ou baixo" como interação: o corte não muda o resultado no modelo reduzido e a resposta entra como o parâmetro `cima: bool` (a UI é sprint 06).

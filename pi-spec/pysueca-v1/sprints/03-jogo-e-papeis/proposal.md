# Proposal — Sprint 03 — Jogo e papéis

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 03 — Jogo e papéis
> **Depende de:** Sprint 02 — Vaza e mão (concluída)

## Por que

Uma `Mao` já roda isolada (`motor.py:65`), mas a mesa não tem memória nem continuidade: nada acumula os pontos por dupla, nada decide a mão seguinte e nada encerra a mesa. Sem o `Jogo`, o servidor (05) não sabe quando parar de pedir jogadas nem o que dizer na tela final, e a corrida até 4 partidas do README (`README.md:24,54`) não existe em código. A rotação de papéis do README item 10 (`README.md:43`) também precisa de um dono: hoje a `Mao` recebe um `embaralhador` fixo, e ninguém o faz andar um assento por mão.

## O que muda

- **`src/pysueca/motor.py`** (modificado) — `Jogo` (a corrida até 4 partidas entre as duplas `assento % 2`), com `preparar(cima)` / `jogar(assento, carta)` / `encerrar_mao()` delegando e acumulando; rotação do embaralhador um assento por mão; fim do jogo ao alcançar 4 partidas. E `Resultado.partidas` (0, 1, 2 ou 4), que a sprint 02 deixou explicitamente para esta.
- **`tests/test_jogo.py`** (novo) — o jogo sem rede, sem `asyncio` e sem Textual: rotação de papéis, acúmulo por dupla, empate 60–60, bandeira e o limite de 4 partidas.

Nenhuma mudança em `carta.py` e `baralho.py`. Nada de rede, `asyncio` ou Textual entra aqui (`docs/adr/0004`).

## Capabilities

### New Capabilities
- `jogo`: a mesa — dono da `Mao` corrente, do placar por dupla, da rotação de papéis por mão e do fim do jogo em 4 partidas.

### Modified Capabilities
- `mao`: a `Requirement: Pontuação e resultado` ganha quanto a mão vale no placar do jogo — 1 partida na vitória normal, 2 no quilo, 4 na bandeira e 0 no empate —, exposto como `Resultado.partidas` (delegado pela sprint 02).

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/motor.py:45-63` | `Resultado` ganha a propriedade `partidas` (1/2/4/0), sem mudar `de_pontos` (`motor.py:54`) |
| `src/pysueca/motor.py:65-128` | `Mao` intocada; `Jogo` a consome e a substitui a cada mão |
| `src/pysueca/motor.py` (final) | arquivo cresce com `Jogo` (~40 linhas); único módulo de regra tocado |
| `src/pysueca/carta.py` | sem mudança |
| `src/pysueca/baralho.py` | sem mudança; o RNG do `Jogo` continua sendo repassado a `Mao`/`Baralho` (sprint 01) |
| `tests/test_motor.py:120-190` | sem mudança; padrão de mão completa reusado no teste novo |
| `tests/test_jogo.py` | arquivo novo |
| `src/pysueca/main.py:52` | intocado; `uv run mypy src` continua vermelho por `App.dark` (pré-existente, sprint 06) |
| `pyproject.toml:6-12` | sem mudança; nenhuma dependência nova (`docs/adr/0004`) |

Consumidores futuros: o `protocolo.py` (04) lê `Jogo.partidas`/`Jogo.encerrado` no snapshot; o servidor (05) chama `Jogo.jogar` e `Jogo.encerrar_mao`; a TUI (06) desenha o placar e a tela final a partir de `Jogo.partidas`/`Jogo.vencedor`.

## Não objetivos

- Protocolo de fio, snapshot e validação de rede — sprint 04. `Jogo` expõe o estado; não o serializa.
- `asyncio`, socket e servidor — sprint 05.
- Tela, placar desenhado e mensagem de fim de jogo — sprint 06.
- Modelar cortador e respondente como estado: a `Mao` já os deriva do embaralhador (dador `(e+3)%4`, cortador `(e+2)%4`, respondente `(e+1)%4`, `design.md` da sprint 02, decisão 4); a rotação cuida de todos ao andar o embaralhador.
- Sorteio do primeiro embaralhador pelo motor: `Jogo(rng, embaralhador=0)` fixa A na primeira mão (`README.md:30`); quem quiser sorteio passa o assento.

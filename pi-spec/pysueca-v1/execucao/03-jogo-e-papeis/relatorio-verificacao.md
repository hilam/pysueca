# Relatório de Verificação — Sprint 03-jogo-e-papeis — Jogo e papéis — 2026-10-12

> **Sprint:** `sprints/03-jogo-e-papeis/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| Partidas que a mão vale | `sprints/03-jogo-e-papeis/specs/mao/spec.md` → Requirement: Pontuação e resultado (CRITICAL) | passou | `test_partidas_que_a_mao_vale` |
| O embaralhador puxa a primeira vaza | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Rotação de papéis (CRITICAL) | passou | `test_embaralhador_puxa_a_primeira_vaza` |
| Papéis andam um assento por mão | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Rotação de papéis (CRITICAL) | passou | `test_papeis_andam_um_assento_por_mao` (mão real + `carta_trunfo in maos[0]`) |
| Jogo.jogar devolve o erro do motor | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Rotação de papéis (EDGE) | passou | `test_jogo_jogar_devolve_o_erro_do_motor` |
| Mão normal soma uma partida à dupla vencedora | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Placar de partidas (CRITICAL) | passou | `test_mao_normal_soma_uma_partida_a_dupla_vencedora` |
| Quilo soma duas partidas à dupla vencedora | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Placar de partidas (CRITICAL) | passou | `test_quilo_soma_duas_partidas_a_dupla_1` |
| EDGE - Empate de 60 a 60 não dá partida | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Placar de partidas (EDGE) | passou | `test_empate_nao_da_partida_a_ninguem` (placar parado + rotação + `encerrado is False`) |
| EDGE - Bandeira encerra o jogo na hora | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo (CRITICAL) | passou | `test_bandeira_encerra_o_jogo_na_hora` |
| Quilo não encerra o jogo | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo (CRITICAL) | passou | `test_quilo_nao_encerra_o_jogo` |
| Jogo acaba ao chegar a 4 partidas | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo (CRITICAL) | passou | `test_jogo_acaba_ao_chegar_a_4_partidas` |
| EDGE - Jogo encerrado não abre nova mão | `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo (EDGE) | passou | `test_jogo_encerrado_nao_abre_nova_mao` |

Nenhum `CRITICAL` falhou; nenhum teste do qa-plan ausente.

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest -q
  uv run --with pytest-cov pytest --cov=pysueca --cov-report=term-missing -q
  uv run ruff check --output-format=concise
  uv run ruff format --check
  uv run mypy src
  ```
- **Saída relevante:**
  ```
  46 passed in 0.07s

  Name                      Stmts   Miss  Cover   Missing
  -------------------------------------------------------
  src/pysueca/__init__.py       2      1    50%   2
  src/pysueca/baralho.py        9      0   100%
  src/pysueca/carta.py         66      0   100%
  src/pysueca/main.py          19     19     0%   1-57
  src/pysueca/motor.py        129      1    99%   183
  -------------------------------------------------------
  TOTAL                       225     21    91%

  ruff check: 4 erros — imagens/get_images.py:1 I001; main.py:14/21/28 RUF012
  ruff format --check: 2 arquivos (main.py, imagens/get_images.py)
  mypy src: main.py:52 error: Cannot determine type of "dark"  [has-type]
  ```
- **Cobertura:** `motor.py` 99% (linha 183 = `vencedor` → `None` enquanto o jogo corre). `carta.py`/`baralho.py` 100%. `main.py` 0% e `imagens/get_images.py` são pré-existentes (sprint 06).
- **Arquivos tocados pela sprint:** `src/pysueca/motor.py` e `tests/test_jogo.py` passam limpos em `ruff check` e `ruff format --check`.

## Gaps / Tech debt

- **Baixa — `motor.py:183` (`Jogo.vencedor is None` enquanto o jogo corre) sem teste dedicado.** O contrato está no `design.md` (decisão 9) e na docstring de `vencedor`; o único caso que exercita o ramo é o `else` de `if not self.encerrado`. Fácil de ancorar (ex.: assert em `test_quilo_nao_encerra_o_jogo`), mas não é `CRITICAL` nem derruba a cobertura abaixo de 80%.
- **Baixa — dívida pré-existente de lint/tipos** em `src/pysueca/main.py` (RUF012 ×3, `mypy:52`) e `src/pysueca/imagens/get_images.py` (I001, format). Já registrada desde a sprint 01; `main.py` é reescrita na sprint 06.
- **Artefato corrigido durante a execução:** o `qa-plan.md` trazia o cenário "quilo soma duas partidas" com placar `41 a 79` (que é vitória normal); corrigido para `29 a 91` no commit `docs(03-jogo-e-papeis): corrige o placar do cenário de quilo no qa-plan`.

## Decisão

- **Status:** Aprovado

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Nenhum `CRITICAL` em falta | — | — |
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (`motor.py:183`) | baixa | uma linha de `motor.py` sem teste; consumida pelo protocolo (04) e TUI (06), que terão seus próprios testes |
| Lint/tipos em `main.py` e `imagens/get_images.py` | baixa | pré-existentes; endereçados na sprint 06 |

> **Próximo passo:** Aprovado → registrar em `LICOES.md` e avançar para a próxima sprint.

# Relatório de Verificação — Sprint 01 — Carta e baralho — 2026-10-12

> **Sprint:** `pi-spec/pysueca-v1/sprints/01-carta-e-baralho/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| Carta formada por naipe e valor | `specs/carta/spec.md` → Requirement: Carta é par de naipe e valor | passou | `test_carta_formada_por_naipe_e_valor` |
| Pontos dos valores com ponto | `specs/carta/spec.md` → Requirement: Pontos por valor | passou | `test_pontos_dos_valores_com_ponto` |
| EDGE - Valor sem ponto vale zero | `specs/carta/spec.md` → Requirement: Pontos por valor (edge case) | passou | `test_valor_sem_ponto_vale_zero` |
| Soma dos pontos do baralho é 120 | `specs/carta/spec.md` → Requirement: Pontos por valor | passou | `test_soma_dos_pontos_do_baralho_e_120` |
| Ás mais forte que Sete | `specs/carta/spec.md` → Requirement: Força independente dos pontos | passou | `test_as_mais_forte_que_sete` |
| EDGE - Força entre cartas de 0 ponto | `specs/carta/spec.md` → Requirement: Força independente dos pontos (edge case) | passou | `test_forca_entre_cartas_de_0_ponto` |
| "7H" ida e volta preserva naipe e valor | `specs/carta/spec.md` → Requirement: Texto ida-e-volta | passou | `test_texto_ida_e_volta_preserva_naipe_e_valor` |
| EDGE - Texto inválido rejeitado | `specs/carta/spec.md` → Requirement: Texto ida-e-volta (edge case) | passou | `test_texto_invalido_rejeitado` |
| Ás de trunfo vence qualquer carta | `specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza | passou | `test_as_de_trunfo_vence_qualquer_carta` (39 cartas × 4 naipes puxados) |
| Entre trunfos vence a maior | `specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza | passou | `test_entre_trunfos_vence_a_maior` |
| Naipe puxado vence o descarte de força maior | `specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza | passou | `test_naipe_puxado_vence_o_descarte_de_forca_maior` |
| Trunfo vence o naipe puxado | `specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza | passou | `test_trunfo_vence_o_naipe_puxado` |
| Baralho tem 40 cartas distintas | `specs/baralho/spec.md` → Requirement: Baralho de 40 cartas | passou | `test_baralho_tem_40_cartas_distintas` |
| Cada naipe tem os 10 valores | `specs/baralho/spec.md` → Requirement: Baralho de 40 cartas | passou | `test_cada_naipe_tem_os_10_valores` |
| Pontos do baralho completo somam 120 | `specs/baralho/spec.md` → Requirement: Baralho de 40 cartas | passou | `test_soma_dos_pontos_do_baralho_e_120` |
| Mesma seed, mesma ordem | `specs/baralho/spec.md` → Requirement: RNG injetado | passou | `test_mesma_seed_mesma_ordem` |
| EDGE - Seeds diferentes embaralham diferente | `specs/baralho/spec.md` → Requirement: RNG injetado (edge case) | passou | `test_seeds_diferentes_embaralham_diferente` |
| Embaralhar preserva as 40 cartas | `specs/baralho/spec.md` → Requirement: Embaralhamento preserva as cartas | passou | `test_embaralhar_preserva_as_40_cartas` |
| EDGE - Embaralha sem o random global | `specs/baralho/spec.md` → Requirement: RNG injetado (edge case) | passou | `test_embaralha_sem_o_random_global` (monkeypatch de `random.shuffle`/`randrange`) |

**19/19** `### Test:` do qa-plan cobertos por `tests/test_carta.py` (18 funções; "Soma dos pontos do baralho é 120" e "Pontos do baralho completo somam 120" compartilham o mesmo teste).

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest -v
  uv run ruff check
  uv run ruff format --check src/pysueca/carta.py src/pysueca/baralho.py tests/test_carta.py
  uv run mypy src
  uv run --with pytest-cov pytest --cov=pysueca --cov-report=term-missing
  uv run --with pytest-cov pytest --cov=pysueca.carta --cov=pysueca.baralho --cov-report=term-missing
  ```
- **Saída relevante:** `18 passed in 0.10s`; `ruff check` limpo nos arquivos da sprint; `mypy src` → 1 erro pré-existente em `src/pysueca/main.py:52` (`App.dark`).
- **Cobertura:** módulos da sprint **97%** (`baralho.py` 100%, `carta.py` 97% — faltam as linhas 75 `Carta.__str__` e 80 `ValueError` do guard de tamanho). Total do repo 78%, puxado por `main.py` 0% (pré-existente, substituído na sprint 06) e `__init__.py` 50%.

## Gaps / Tech debt

- `Carta.__str__` (linha 75) sem teste — a TUI (sprint 06) é quem vai usá-lo; baixa prioridade.
- Guard `if len(texto) != 2` (linha 80) sem teste — testar `Carta.de_texto("7")` fecharia o ramo; baixa prioridade.
- `uv run mypy src` não fica limpo por `main.py:52` — pré-existente, endereçado na sprint 06 que reescreve `main.py`.
- Ciclo TDD: 4 dos 12 cenários de `carta.py` (pontos, força, texto) entraram como cobertura porque o módulo nasceu completo; RED genuíno em 2.1, 2.4, 2.22 e 2.28. Registrado em `tasks.md` → Notas de Execução.

## Decisão

- **Status:** Aprovado

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste do guard de tamanho de `de_texto` (linha 80) | baixa | ramo defensivo de 1 linha; próximo teste de `carta.py` cobre |
| Teste de `Carta.__str__` (linha 75) | baixa | sem consumidor até a sprint 06; cobrir quando a TUI usar |
| `mypy src` vermelho por `main.py:52` (pré-existente) | baixa | sprint 06 substitui `main.py`; não afeta o motor |

> **Próximo passo:** Aprovado → `LICOES.md` e `state.sh finish 01-carta-e-baralho` + `advance sprints`.

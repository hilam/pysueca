# Relatório de Verificação — Sprint 02-vaza-e-mao — Vaza e mão — 2026-10-12

> **Sprint:** `sprints/02-vaza-e-mao/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 02 — Vaza e mão
> **Período:** 2026-10-12 — 2026-10-12
> **Branch:** `feat/pysueca-v1-02-vaza-e-mao` (29 commits: 1 planejamento + 1 transição + ciclos test/feat + refactor + style + docs)

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| Test: Assento com o naipe puxado é obrigado a jogá-lo | `specs/vaza/spec.md` → Requirement: Seguir o naipe puxado (CRITICAL) | passou | `tests/test_motor.py::test_assento_com_o_naipe_puxado_e_obrigado_a_joga_lo` |
| Test: Assento sem o naipe puxado pode jogar qualquer carta (trunfar) | `specs/vaza/spec.md` → Requirement: Seguir o naipe puxado (CRITICAL) | passou | `::test_sem_o_naipe_puxado_pode_jogar_qualquer_carta` |
| Test: Ao puxar, qualquer carta da mão é aceita | `specs/vaza/spec.md` → Requirement: Seguir o naipe puxado (CRITICAL) | passou | `::test_ao_puxar_qualquer_carta_e_aceita` |
| Test: Trunfo vence o naipe puxado | `specs/vaza/spec.md` → Requirement: Vencedor da vaza (CRITICAL) | passou | `::test_trunfo_vence_o_naipe_puxado` |
| Test: Entre trunfos vence a maior | `specs/vaza/spec.md` → Requirement: Vencedor da vaza (CRITICAL) | passou | `::test_entre_trunfos_vence_a_maior` |
| Test: Maior força do naipe puxado vence os descartes | `specs/vaza/spec.md` → Requirement: Vencedor da vaza (CRITICAL) | passou | `::test_maior_forca_do_naipe_puxado_vence_os_descartes` |
| Test: Preparação distribui 10 cartas por assento | `specs/mao/spec.md` → Requirement: Preparação da mão (CRITICAL) | passou | `::test_preparacao_distribui_10_cartas_por_assento` |
| Test: A carta do trunfo fica com o dador | `specs/mao/spec.md` → Requirement: Preparação da mão (CRITICAL) | passou | `::test_carta_do_trunfo_fica_com_o_dador` (embaralhador 0 → dador 3) |
| Test: Cima ou baixo escolhe a ponta do baralho | `specs/mao/spec.md` → Requirement: Preparação da mão (CRITICAL) | passou | `::test_cima_ou_baixo_escolhe_a_ponta_do_baralho` (comparado a `Baralho(Random(42))` de referência) |
| Test: Quem levou a vaza puxa a seguinte | `specs/mao/spec.md` → Requirement: Sequência de vazas (CRITICAL) | passou | `::test_quem_levou_a_vaza_puxa_a_seguinte` |
| Test: Mão completa são 10 vazas e esvazia as mãos | `specs/mao/spec.md` → Requirement: Sequência de vazas (CRITICAL) | passou | `::test_mao_completa_sao_10_vazas_e_esvazia_as_maos` (seed 7, 10 vazas) |
| Test: Jogada fora da vez devolve erro | `specs/mao/spec.md` → Requirement: Jogada ilegal devolve erro (EDGE) | passou | `::test_jogada_fora_da_vez_devolve_erro` |
| Test: Carta fora da mão devolve erro | `specs/mao/spec.md` → Requirement: Jogada ilegal devolve erro (EDGE) | passou | `::test_carta_fora_da_mao_devolve_erro` |
| Test: Jogada ilegal não altera o estado | `specs/mao/spec.md` → Requirement: Jogada ilegal devolve erro (EDGE) | passou | `::test_jogada_ilegal_nao_altera_o_estado` (snapshot de `vez`/`maos`/`vaza` antes e depois) |
| Test: Pontuação da mão jogada | `specs/mao/spec.md` → Requirement: Pontuação e resultado (CRITICAL) | passou | `::test_pontuacao_da_mao_jogada` (88–32, soma 120, `NORMAL`) |
| Test: EDGE - Resultado pelos limites do README | `specs/mao/spec.md` → Requirement: Pontuação e resultado (EDGE) | passou | `::test_resultado_pelos_limites_do_readme` (60/61/90/91/119/120) |

**Cobertura:** 16/16 cenários do qa-plan têm teste homônimo e verde.

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest -v 2>&1 | tail -n 45
  uv run ruff check src/pysueca/motor.py tests/test_motor.py
  uv run ruff format --check src/pysueca/motor.py tests/test_motor.py
  uv run mypy src
  uv run python -m trace --count --missing ...   # cobertura stdlib (pytest-cov não instalado)
  ```
- **Saída relevante:** `35 passed in 0.08s` (19 em `test_carta.py` + 16 em `test_motor.py`), 0 falhas, 0 erros. `All checks passed!` (ruff) e `2 files already formatted` no escopo do módulo novo.
- **Cobertura:** `src/pysueca/motor.py` — **100% das linhas executáveis** (100 statements contados, 0 marcados `>>>>>>` pelo `trace`). Nenhum ramo defensivo descoberto.
- **Tipos:** `uv run mypy src` → 1 erro **pré-existente** `src/pysueca/main.py:52` (`App.dark`); `motor.py` limpo.
- **Lint global:** 4 erros **pré-existentes** fora do escopo — `main.py` RUF012 ×3 e `src/pysueca/imagens/get_images.py` I001 (sprint 06 reescreve `main.py`). `main.py`/`get_images.py` seguem desformatados.

### Revisão de contrato (spec → código)

- `jogada_legal(mao, naipe_puxado, carta)` cobre os dois ramos: segue o naipe; ou libera quando a mão não tem o naipe (trunfar/descartar). Ao puxar (`vaza is None`) o naipe não é checado e `Vaza.naipe_puxado` = naipe da carta.
- `Vaza.vencedor` agrega `Carta.vence` (sprint 01) — nenhuma regra de precedência reescrita; confirmado pelos cenários V4–V6.
- `Mao.preparar`: `dador = (embaralhador + 3) % 4`; trunfo é a ponta (`0` se `cima`, `-1` se baixo); rodízio dá 9 cartas ao dador + a carta do trunfo = 10; total particionado em 40.
- `Mao._validar` valida vez → posse → naipe **antes** de qualquer mutação (o refactor da task 7.1 centralizou as três checagens), o que sustenta o cenário "jogada ilegal não altera o estado".
- `pontos` por dupla (`assento % 2`); `resultado` delega a `Resultado.de_pontos` (60 empate / 61–90 normal / 91–119 quilo / 120 bandeira).

## Gaps / Tech debt

- **Processo (TDD):** dois cenários marcados RED no `tasks.md` nasceram verdes por implementação adjacente já presente — `4.7` (trunfar sem o naipe) e `5.4` (quilo/bandeira), além dos já previstos `2.4`/`6.7`. Não é falha de comportamento (cobertura 100%), mas repete a lição da sprint 01 ("módulo nasce completo demais"). Nenhuma ação de código.
- **Doc drift (baixa):** `PLANO-PYSUECA-V1.md` ainda descreve "`puxar`/`jogar` devolvendo erro", mas `puxar` foi fundido em `Mao.jogar` (decisão 2 do `design.md`, confirmada no grill). O PLANO não foi atualizado.
- **Pré-existentes, fora de escopo:** `mypy src` vermelho por `main.py:52`; 4 erros de `ruff check` e 2 arquivos desformatados (`main.py`, `imagens/get_images.py`) — endereçados na sprint 06.
- **Decisão de modelo (aceita):** ordem da distribuição "cima/baixo" não modelada além da ponta do baralho (risco declarado no PLANO; mitigação em `design.md` decisão 4 e `docs/adr/0003`). Não é gap.

## Decisão

- **Status:** Aprovado

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Registrar em LICOES.md a recorrência de cenários "RED esperado verde" (4.7/5.4) | média | repete o vício de escrever o módulo inteiro antes do 1º vermelho; reduz o valor de sinal dos testes das sprints 03–06 |
| Atualizar a linha de decisão arquitetural do PLANO (`puxar` fundido em `jogar`) | baixa | leitura do PLANO diverge do `design.md`; sem custo de execução |
| Fechar `/pi-verificar` e seguir para `/pi-sprint-propor` (sprint 03) | — | nenhum |

> **Próximo passo:** Aprovado → `LICOES.md` e `state.sh finish 02-vaza-e-mao` + `state.sh advance sprints`.

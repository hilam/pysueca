# Relatório de Verificação — Sprint 04-protocolo — Protocolo — 2026-10-12

> **Sprint:** `sprints/04-protocolo/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| Test: entrar faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_entrar_faz_ida_e_volta` |
| Test: responder faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_responder_faz_ida_e_volta` |
| Test: jogar faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_jogar_faz_ida_e_volta` |
| Test: estado faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_estado_faz_ida_e_volta` |
| EDGE - linha malformada vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_linha_malformada_vira_erro` |
| EDGE - tipo desconhecido vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_tipo_desconhecido_vira_erro` |
| EDGE - campo faltando vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_campo_faltando_vira_erro` |
| EDGE - campo extra vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_campo_extra_vira_erro` |
| Test: nome é normalizado | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_nome_e_normalizado` |
| EDGE - nome inválido vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_nome_invalido_vira_erro` |
| EDGE - linha acima do teto é fatal | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Teto de bytes por linha | passou | `test_linha_acima_do_teto_e_fatal` |
| EDGE - linha no limite é aceita | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Teto de bytes por linha | passou | `test_linha_no_limite_e_aceita` |
| EDGE - nenhum outro erro é fatal | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Teto de bytes por linha | passou | `test_nenhum_outro_erro_e_fatal` |
| Test: snapshot traz a própria mão | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento | passou | `test_snapshot_traz_a_propria_mao` |
| EDGE - snapshot traz só a contagem das outras mãos | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento | passou | `test_snapshot_traz_so_a_contagem_das_outras_maos` |
| EDGE - snapshot reflete a mesa | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento | passou | `test_snapshot_reflete_a_mesa` |
| Test: snapshot diz quem deve responder | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento | passou | `test_snapshot_diz_quem_deve_responder` |
| EDGE - jogada fora da vez vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Erro de jogada formatado | passou | `test_jogada_fora_da_vez_vira_erro` |
| EDGE - carta fora da mão vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Erro de jogada formatado | passou | `test_carta_fora_da_mao_vira_erro` |
| EDGE - não seguir o naipe vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Erro de jogada formatado | passou | `test_nao_seguir_o_naipe_vira_erro` |

**20/20 cenários com teste e verde.** Nenhum `CRITICAL` falhou.

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest -q
  uv run pytest tests/test_protocolo.py -q
  uv run ruff check --output-format concise
  uv run mypy src
  # cobertura via stdlib (sem pytest-cov no projeto):
  uv run python -c 'import trace, pytest; ...'   # trace.Trace sobre tests/test_protocolo.py
  ```
- **Saída relevante:**
  - `uv run pytest -q` → `66 passed in 0.10s` (46 pré-existentes + 20 novos).
  - `uv run pytest tests/test_protocolo.py -q` → `20 passed in 0.14s`.
  - `uv run ruff check` → 4 erros, todos pré-existentes e fora da sprint: `main.py:14,21,28` (RUF012) e `imagens/get_images.py:1` (I001). `protocolo.py` e `test_protocolo.py` limpos.
  - `uv run mypy src` → 1 erro pré-existente: `main.py:52 Cannot determine type of "dark"`. `protocolo.py` limpo.
- **Cobertura:** `src/pysueca/protocolo.py` **97.9%** (143/146 linhas executáveis; 3 não cobertas: `_para_dados` ramo `erro`, o `return "campo_faltando"` da checagem de tipo em `_validar` e o `return Erro(dados["motivo"])` da desserialização de `erro`). Demais módulos do motor permanecem cobertos pelas sprints 01–03.

## Gaps / Tech debt

- **Round-trip de `erro` não testado (média):** o `Requirement: Mensagens de fio` diz "cada mensagem SHALL fazer ida-e-volta" e lista `erro` entre os tipos, mas o `qa-plan.md` (seguindo o entregável do PLANO) só cobre `entrar`/`responder`/`jogar`/`estado`. São as 3 linhas não cobertas: `serializar(Erro(...))` e `desserializar(b'{"tipo":"erro",...}')` nunca rodam nos testes. O servidor (05) só envia `erro`, então a lacuna é do caminho de saída, não do caminho jogado.
- **Campo com tipo errado não tem teste direto (baixa):** o `qa-plan.md` cita o caso em "Casos Limite" (`"carta": 7`, `"cima": "sim"`), mas nenhum `### Test:` o exercita — é o `return "campo_faltando"` de `_validar` não coberto.
- **Sem ferramenta de cobertura no projeto (baixa):** `pytest-cov`/`coverage` não estão nas dev-deps; a cobertura deste relatório saiu de `trace` (stdlib). Se a cobertura for critério recorrente, vale adicionar `pytest-cov` ao grupo `dev` (fora do escopo desta sprint).

## Decisão

- **Status:** Retrabalho

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste de ida-e-volta de `erro` (serializar + desserializar) — **em retrabalho** | média | caminho de saída usado pela 05 fica sem teste; 3 linhas descobertas |
| Teste de campo com tipo errado — **em retrabalho** | baixa | ramo defensivo de 1 linha sem cobertura direta |
| Adicionar `pytest-cov` às dev-deps — **em retrabalho** | baixa | cobertura medida por `trace` manual a cada verificação |
| `mypy src` (`main.py:52`) e `ruff check` (`main.py`, `imagens/get_images.py`) | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na sprint 06 |

> **Próximo passo:** Retrabalho → `/pi-grill` sprint `04-protocolo` (3 itens acima); depois `/pi-atualizar` e `/pi-sprint-executar`.

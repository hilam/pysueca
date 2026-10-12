# Relatório de Verificação — Sprint 04-protocolo — Protocolo — 2026-10-12

> **Sprint:** `sprints/04-protocolo/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12
> **Nota:** este relatório é a **re-verificação** que sucede o retrabalho das fases 9–11 do `tasks.md` (o primeiro parecer foi "Retrabalho" nos 3 itens de cobertura/dependência).

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| Test: entrar faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_entrar_faz_ida_e_volta` |
| Test: responder faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_responder_faz_ida_e_volta` |
| Test: jogar faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_jogar_faz_ida_e_volta` |
| Test: estado faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_estado_faz_ida_e_volta` |
| Test: erro faz ida-e-volta | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio | passou | `test_erro_faz_ida_e_volta` — **novo no retrabalho** |
| EDGE - linha malformada vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_linha_malformada_vira_erro` |
| EDGE - tipo desconhecido vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_tipo_desconhecido_vira_erro` |
| EDGE - campo faltando vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_campo_faltando_vira_erro` |
| EDGE - campo extra vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_campo_extra_vira_erro` |
| EDGE - campo com tipo errado vira erro | `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável | passou | `test_campo_com_tipo_errado_vira_erro` — **novo no retrabalho** |
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

**22/22 cenários com teste e verde.** Nenhum `CRITICAL` falhou.

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest --cov=pysueca --cov-fail-under=80 -q
  uv run ruff check --output-format concise
  uv run ruff format --check src/pysueca/protocolo.py tests/test_protocolo.py
  uv run mypy src
  ```
- **Saída relevante:**
  - `uv run pytest --cov=pysueca --cov-fail-under=80 -q` → `68 passed`; `Required test coverage of 80% reached. Total coverage: 93.63%`.
  - `uv run ruff check` → 4 erros pré-existentes: `main.py:14,21,28` (RUF012) e `docs/imagens/get_images.py:1` (I001). `protocolo.py` e `test_protocolo.py` limpos.
  - `uv run ruff format --check` (arquivos da sprint) → `2 files already formatted`.
  - `uv run mypy src` → 1 erro pré-existente: `main.py:52 Cannot determine type of "dark"`; 6 arquivos checados (inclui `protocolo.py`).
- **Cobertura por arquivo:** `protocolo.py` **100%** (89/89), `motor.py` 100%, `carta.py` 100%, `baralho.py` 100%, `__init__.py` 50%, `main.py` 0% (sem teste até a 06). **Total 93,63%**, acima do gate de 80%.

## Gaps / Tech debt

- **`main.py` em 0% e `__init__.py` em 50% (baixa):** fora do escopo da sprint; `main.py` é reescrita na sprint 06 e a versão em `__init__.py` não é exercitada.
- **Lint/tipos pré-existentes (baixa):** `main.py` RUF012 ×3 + `mypy:52` e `docs/imagens/get_images.py` I001 (agora no caminho novo) — registrados desde a sprint 01, endereçados na sprint 06.
- **`get_images.py` saiu do pacote mas segue sob `ruff check` (baixa):** o `git mv` tirou-o do escopo de `--cov=pysueca`, mas o linter varre o repositório inteiro; o I001 continua até a sprint 06 (ou até um `exclude` no `pyproject.toml`, se desejado).

## Decisão

- **Status:** Aprovado

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Nenhum item de retrabalho do primeiro parecer em aberto | — | os 3 itens (round-trip de `erro`, campo com tipo errado, `pytest-cov` + gate) foram implementados nas fases 9–11 |
| `main.py` em 0% de cobertura | baixa | `main.py` é reescrita e testada na sprint 06; o gate global de 80% segue atingido |
| `ruff`/`mypy` pré-existentes em `main.py` e `docs/imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na sprint 06 |
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (arrastado da sprint 03) | baixa | contrato documentado sem teste; protocolo (04) e TUI (06) trazem os seus |

> **Próximo passo:** Aprovado → `LICOES.md` e avançar para a próxima sprint (`/pi-sprint-propor`, sprint 05 — Servidor). Retrabalho → `/pi-grill` sprint `04-protocolo`.

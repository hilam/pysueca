# Relatório de Verificação — Sprint 05-servidor — Servidor — 2026-10-12

> **Sprint:** `sprints/05-servidor/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| Test: entrar senta no primeiro assento livre | `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Mesa autoritativa por assentos | passou | `test_entrar_senta_no_primeiro_assento_livre` |
| EDGE - nome já sentado e ativo é recusado | idem → (edge case) | passou | `test_nome_ja_sentado_e_ativo_e_recusado` |
| EDGE - mesa cheia recusa o quinto | idem → (edge case) | passou | `test_mesa_cheia_recusa_o_quinto` |
| EDGE - não sentado é recusado | idem → (edge case) | passou | `test_nao_sentado_e_recusado` |
| Test: quatro assentos abrem a pergunta cima ou baixo | idem → Requirement: Início da mão pelo respondente | passou | `test_quatro_assentos_abrem_a_pergunta_cima_ou_baixo` |
| Test: responder prepara a mão e distribui dez cartas | idem → Requirement: Início da mão pelo respondente | passou | `test_responder_prepara_a_mao_e_distribui_dez_cartas` |
| EDGE - responder fora de hora é recusado | idem → (edge case) | passou | `test_responder_fora_de_hora_e_recusado` |
| Test: jogada ilegal vira erro só para quem jogou | idem → Requirement: Jogada validada pelo motor | passou | `test_jogada_ilegal_vira_erro_so_para_quem_jogou` |
| Test: jogada legal chega aos quatro | idem → Requirement: Jogada validada pelo motor | passou | `test_jogada_legal_chega_aos_quatro` |
| Test: a décima vaza conta a mão | idem → Requirement: Jogada validada pelo motor | passou | `test_a_decima_vaza_conta_a_mao` |
| EDGE - mão nova volta a perguntar cima ou baixo | idem → (edge case) | passou | `test_mao_nova_volta_a_perguntar_cima_ou_baixo` |
| Test: o jogo encerrado não abre mão nova | idem → Requirement: Jogada validada pelo motor | passou | `test_o_jogo_encerrado_nao_abre_mao_nova` |
| EDGE - mensagem de direção errada é recusada | idem → (edge case) | passou | `test_mensagem_de_direcao_errada_e_recusada` |
| Test: queda congela a mesa e avisa os outros três | idem → Requirement: Queda congela a mesa e reserva o assento | passou | `test_queda_congela_a_mesa_e_avisa_os_outros_tres` |
| EDGE - mesa congelada recusa jogadas | idem → (edge case) | passou | `test_mesa_congelada_recusa_jogadas` |
| Test: reconexão com o mesmo nome retoma o assento | idem → Requirement: Queda congela a mesa e reserva o assento | passou | `test_reconexao_com_o_mesmo_nome_retoma_o_assento` |
| Test: linha acima do teto fecha aquela conexão | idem → Requirement: Linha acima do teto fecha só aquela conexão | passou | `test_linha_acima_do_teto_fecha_aquela_conexao` |
| EDGE - os outros três seguem na mesa | idem → (edge case) | passou | `test_os_outros_tres_seguem_na_mesa` |
| Test: estado carrega os assentos ausentes | `sprints/05-servidor/specs/protocolo/spec.md` → Requirement: Snapshot por assento | passou | `test_estado_carrega_os_assentos_ausentes` |
| EDGE - ausentes com tipo errado vira erro | idem → (edge case) | passou | `test_ausentes_com_tipo_errado_vira_erro` |

20/20 testes do `qa-plan.md` existem e passam (`tests/test_servidor.py` ×18, `tests/test_protocolo.py` ×2). Nenhum `### Test:` sem caso correspondente.

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest --cov=pysueca --cov-fail-under=80 -q
  uv run ruff check --output-format concise
  uv run ruff format --check
  uv run mypy src
  uv run ruff check src/pysueca/servidor.py src/pysueca/protocolo.py tests/test_servidor.py tests/test_protocolo.py
  ```
- **Saída relevante:**
  - `88 passed in 4.32s`
  - `Required test coverage of 80% reached. Total coverage: 95.28%`
  - Escopo da sprint: `All checks passed!`, `4 files already formatted`, `mypy` → `Success: no issues found in 2 source files`.
  - Global pré-existente: `ruff check` → 4 erros (`src/pysueca/main.py:14,21,28` RUF012; `docs/imagens/get_images.py:1` I001); `ruff format --check` → 2 arquivos (`main.py`, `get_images.py`); `mypy src` → `main.py:52`.
- **Cobertura:** 95,28% total; `servidor.py` 100%, `protocolo.py` 100%, `motor.py` 100%, `carta.py`/`baralho.py` 100%. Fora: `main.py` 0% (esqueleto, reescrito na 06) e `__init__.py` 50% — ambos pré-existentes.

## Gaps / Tech debt

- **Motivo `fora_de_hora` (resolvido nesta verificação):** a `design.md` decisão 8 listava cinco motivos de assento e a recusa de `responder` fora de hora não tinha motivo nomeado. Durante esta verificação o motivo `fora_de_hora` foi incorporado à decisão 8 e ao `spec.md` (mesa incompleta → `mesa_incompleta`; não é o respondente / mão já preparada → `fora_de_hora`). Código, spec e design agora batem; sem débito.
- **Dívida pré-existente (baixa):** `ruff`/`mypy` vermelhos em `src/pysueca/main.py` e `docs/imagens/get_images.py` — registrada desde a sprint 01 e endereçada na sprint 06. Nenhum débito novo introduzido pela 05.
- **Arrastado de 03/04 (baixa):** contrato `Jogo.vencedor is None` enquanto o jogo corre segue sem teste próprio.

## Decisão

- **Status:** Aprovado

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Motivo `fora_de_hora` — incorporado à decisão 8 do `design.md` e ao `spec.md` na verificação | baixa | resolvido; rastreabilidade fechada, sem retrabalho |
| `ruff`/`mypy` pré-existentes em `main.py` e `docs/imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na 06 |
| `Jogo.vencedor is None` sem teste próprio | baixa | contrato documentado; protocolo (04) e TUI (06) trazem os seus |
| `main.py` 0% / `__init__.py` 50% de cobertura | baixa | gate global segue com folga (95,28%); some na 06 |

> **Próximo passo:** Aprovado → registrar em `LICOES.md` e avançar para a sprint 06.

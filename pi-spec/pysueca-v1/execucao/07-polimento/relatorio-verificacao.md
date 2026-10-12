# Relatório de Verificação — Sprint 07-polimento — Polimento — 2026-10-12

> **Sprint:** `sprints/07-polimento/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12
> **Branch:** `feat/pysueca-v1-07-polimento` (24 commits; `git log main..HEAD`)

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| todo código de motivo do v1 vira frase de jogador | `specs/avisos/spec.md` → Motivo de recusa em frase de jogador | passou | `test_todo_codigo_de_motivo_do_v1_vira_frase_de_jogador`; loop sobre `ErroJogada` + 13 códigos literais, compara com a frase genérica (motivo novo do motor fica vermelho) |
| o nome em uso vira frase na tela | `specs/avisos/spec.md` → Motivo de recusa em frase de jogador | passou | `test_erro_do_servidor_aparece_sem_derrubar_o_app`; `Esse nome já está em uso nesta mesa` no `#aviso`, `nome_em_uso` ausente, snapshot seguinte limpa |
| EDGE - o JSON inválido vira frase | `specs/avisos/spec.md` → Motivo de recusa em frase de jogador | passou | `test_mensagem_invalida_do_fio_nao_derruba_o_app`; `#aviso` com `A mesa mandou uma mensagem que não deu para ler`, `json_invalido` ausente |
| EDGE - motivo desconhecido não vaza código nem derruba a tela | `specs/avisos/spec.md` → Motivo de recusa em frase de jogador | passou | `test_motivo_desconhecido_nao_vaza_codigo_nem_derruba_a_tela`; pura (`== "A mesa recusou o pedido"`) + `Erro("bug_novo")` na tela |
| o fim do jogo aparece na mesa | `specs/fim-de-jogo/spec.md` → Fim de jogo na tela | passou | `test_o_fim_do_jogo_aparece_na_mesa`; `Fim de jogo`, `Ana e Caio`, `4 x 2` |
| a mesa encerrada não anuncia vez | `specs/fim-de-jogo/spec.md` → Fim de jogo na tela | passou | `test_a_mesa_encerrada_nao_anuncia_vez`; snapshot com `vez=0` e `encerrado=True` → sem `Sua vez` |
| a mesa encerrada não manda jogar | `specs/fim-de-jogo/spec.md` → Fim de jogo na tela | passou | `test_a_mesa_encerrada_nao_manda_jogar`; `Enter` com mão cheia → `TimeoutError` (nenhum `Jogar` no falso) |
| EDGE - o nome ausente cai para a dupla | `specs/fim-de-jogo/spec.md` → Fim de jogo na tela | passou | `test_o_nome_ausente_cai_para_a_dupla`; `dupla 1–3`, sem `None` |
| EDGE - o jogo em andamento segue mostrando o placar simples | `specs/fim-de-jogo/spec.md` → Fim de jogo na tela | passou | `test_o_jogo_em_andamento_segue_mostrando_o_placar_simples`; `Placar: 1 x 2`, sem `Fim de jogo` (cobertura declarada) |
| as teclas de jogo aparecem no rodapé | `specs/atalhos/spec.md` → Teclas de jogo visíveis no rodapé | passou | `test_as_teclas_de_jogo_aparecem_no_rodape`; `FooterKey` visíveis: `←`/`→`/`⏎` + `^q`/Sair |
| d alterna o tema | `specs/atalhos/spec.md` → Tema claro e escuro | passou | `test_d_alterna_o_tema`; `d`/Tema no rodapé e `app.theme` `textual-dark` → `textual-light` → `textual-dark` |
| EDGE - o tema não muda a cor do naipe | `specs/atalhos/spec.md` → Tema claro e escuro | passou | `test_o_tema_nao_muda_a_cor_do_naipe`; markup fixo `[red]7♥[/red]` / `[red]A♦[/red]` (cobertura declarada) |
| congelado, a recusa do servidor vira frase de jogador | `specs/cliente/spec.md` → Tela de queda | passou | `test_congelado_o_cliente_ainda_manda_e_o_servidor_recusa`; `Jogar` sai, frase no `#aviso`, `mesa_congelada` ausente |
| EDGE - o erro do servidor aparece como frase | `specs/cliente/spec.md` → Conexão em worker de tela | passou | assert de `test_fora_da_vez_o_servidor_decide` (`A mesa não esperava essa jogada agora`, código ausente); mesmo ramo do nome em uso (cobertura declarada) |

NÃO TESTÁVEL (declarado no qa-plan): `specs/comando/spec.md` → os dois scenarios de `README.md` são prosa; conferidos na leitura manual (task 9.5) e no roteiro manual de quatro terminais (task 9.6, executado pelo operador com sucesso em 2026-10-12).

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest -q                                  # 127 passed
  uv run ruff check                                 # All checks passed!
  uv run ruff format --check                        # 74 files already formatted
  uv run mypy src                                   # Success: no issues found in 7 source files
  uv run pytest --cov=pysueca --cov-fail-under=80   # 98.21%, gate de 80% atendido
  # os 14 testes do qa-plan isolados: 14 passed
  ```
- **Saída relevante:** `127 passed in 14.99s`; cobertura `main.py 97%`, `TOTAL 98.21%`; os 14 testes mapeados passam juntos em 2.98s.
- **Cobertura:** 98% (gate 80%).
- **Superfície tocada** (`git diff --stat main..HEAD`): `src/pysueca/main.py` (+61/-18), `tests/test_cliente.py`, `README.md`, `AGENTS.md`. **`protocolo.py`, `motor.py`, `servidor.py` intactos** — o fio e as regras não mudaram (ADR 0002/0001 preservados), como a spec de `avisos` exige.
- **RED comprovado por reversão** (`main.py` anterior, restaurado em seguida, diff líquido zero):
  - `7404a39:src/pysueca/main.py` (antes do `MOTIVOS`): `ImportError: cannot import name 'frase_do_motivo'`;
  - `39b7d80:src/pysueca/main.py` (antes do fim de jogo): `4 failed` — `o_fim_do_jogo_aparece_na_mesa`, `a_mesa_encerrada_nao_anuncia_vez`, `a_mesa_encerrada_nao_manda_jogar`, `o_nome_ausente_cai_para_a_dupla`.
- **Determinismo:** nenhum `sleep` em `tests/test_cliente.py`; os testes de tela usam o `ServidorFalso` e `pilot.pause()`.
- **Códigos de fio na tela:** os únicos usos de código cru em `tests/test_cliente.py` são `not in` (4 asserts) e a lista de motivos do teste de tradução — nenhum assert espera código visível.

## Gaps / Tech debt

- `o fim do jogo aparece na mesa` prova o render puro de `desenhar_mesa`; o caminho snapshot→`#mesa` é exercido pelos demais testes de tela (o `update` do painel não muda nesta sprint). Um teste de tela com `encerrado` no `#mesa` seria prova redundante.
- Casos-limite do qa-plan sem teste próprio, declarados como tal: `encerrado` com `vencedor` nulo (guard de uma linha, `main.py`), `d` com o modal cima ou baixo aberto, prioridade queda vs. erro no `#aviso` (o teste da mesa congelada não fixa a contagem de frases).
- `src/pysueca/__init__.py` e os ramos defensivos de `servidor.py`/`main.py` seguem fora do escopo (5 linhas em cada), arrastados das sprints 05/06 e já registrados em `LICOES.md`.

## Decisão

- **Status:** Aprovado

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Nenhum item CRITICAL em aberto; os 14 testes do qa-plan passam e a suite está verde | — | — |
| Teste de tela do fim de jogo (`#mesa` com snapshot `encerrado`) em vez do render puro | baixa | o render puro já cobre a linha; o wiring do painel não muda nesta sprint |
| Casos-limite sem teste (vencedor nulo, `d` com modal, prioridade queda/erro) | baixa | ramos defensivos ou de convivência de avisos; nenhum caminho de jogo quebrado |

> **Próximo passo:** Aprovado → `LICOES.md` e avançar. Não há retrabalho de alta criticidade.

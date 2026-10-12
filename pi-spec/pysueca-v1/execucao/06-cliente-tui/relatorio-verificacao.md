# Relatório de Verificação — Sprint 06-cliente-tui — Cliente TUI — 2026-10-12

> **Sprint:** `sprints/06-cliente-tui/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12 — 2026-10-12
> **Nota:** este relatório é a **re-verificação** que sucede o retrabalho da seção 11 do `tasks.md` (o primeiro parecer foi "Retrabalho" na lacuna média do `b` e nos ramos de cobertura do cliente).

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| o cliente manda entrar com o nome | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_o_cliente_manda_entrar_com_o_nome` |
| o cliente se reconhece pelo nome | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_o_cliente_se_reconhece_pelo_nome` |
| EDGE - erro do servidor aparece sem derrubar o app | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_erro_do_servidor_aparece_sem_derrubar_o_app` |
| EDGE - mensagem inválida do fio não derruba o app | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_mensagem_invalida_do_fio_nao_derruba_o_app` |
| EDGE - sem servidor o cliente avisa e segue | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_sem_servidor_o_cliente_avisa_e_segue` |
| EDGE - o fim da conexão vira aviso | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_o_fim_da_conexao_vira_aviso` (novo) |
| EDGE - o teto do leitor vira aviso | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_o_teto_do_leitor_vira_aviso` (novo) |
| tela de espera mostra N de 4 assentos | `specs/cliente/spec.md` → Espera pela mesa completa | passou | `test_tela_de_espera_mostra_n_de_4_assentos` |
| os assentos mostram a contagem de cartas | `specs/cliente/spec.md` → Espera pela mesa completa | passou | `test_os_assentos_mostram_a_contagem_de_cartas` |
| os assentos contam os nomes com um assento vago no meio | `specs/cliente/spec.md` → Espera pela mesa completa | passou | `test_os_assentos_contam_os_nomes_com_um_assento_vago_no_meio` (novo) |
| a mão desenha as cartas com o naipe colorido | `specs/cliente/spec.md` → Mão de cartas em texto | passou | `test_a_mao_desenha_as_cartas_com_o_naipe_colorido` |
| a mesa mostra trunfo, vaza e placar | `specs/cliente/spec.md` → Mão de cartas em texto | passou | `test_a_mesa_mostra_trunfo_vaza_e_placar` |
| a mesa desenha a vaza vazia e a vaza cheia | `specs/cliente/spec.md` → Mão de cartas em texto | passou | `test_a_mesa_desenha_a_vaza_vazia_e_a_vaza_cheia` (novo) |
| ←/→ movem a seleção e Enter joga a carta | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_setas_movem_a_selecao_e_enter_joga_a_carta` |
| EDGE - a seleção não passa dos limites da mão | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_a_selecao_nao_passa_dos_limites_da_mao` |
| EDGE - fora da vez o servidor decide | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_fora_da_vez_o_servidor_decide` |
| EDGE - a seleção volta à primeira carta com a mão nova | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_a_selecao_volta_a_primeira_carta_com_a_mao_nova` |
| EDGE - com a mão vazia nada é jogado | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_com_a_mao_vazia_nada_e_jogado` (ampliado com `←`/`→`) |
| cima ou baixo abre na tela do respondente | `specs/cliente/spec.md` → Pergunta cima ou baixo | passou | `test_cima_ou_baixo_abre_na_tela_do_respondente` |
| cima ou baixo responde | `specs/cliente/spec.md` → Pergunta cima ou baixo | passou | `test_cima_ou_baixo_responde` (ampliado com `b`) |
| EDGE - quem não é o respondente não vê o diálogo | `specs/cliente/spec.md` → Pergunta cima ou baixo | passou | `test_quem_nao_e_o_respondente_nao_ve_o_dialogo` |
| a queda aparece na tela | `specs/cliente/spec.md` → Tela de queda | passou | `test_a_queda_aparece_na_tela` |
| EDGE - reconexão limpa a tela de queda | `specs/cliente/spec.md` → Tela de queda | passou | `test_reconexao_limpa_a_tela_de_queda` |
| EDGE - congelado o cliente ainda manda e o servidor recusa | `specs/cliente/spec.md` → Tela de queda | passou | `test_congelado_o_cliente_ainda_manda_e_o_servidor_recusa` |
| o cliente lê nome, host e porta | `specs/comando/spec.md` → Cliente na linha de comando | passou | `test_o_cliente_le_nome_host_e_porta` |
| o cliente usa os defaults | `specs/comando/spec.md` → Cliente na linha de comando | passou | `test_o_cliente_usa_os_defaults` |
| o servidor lê host e porta | `specs/comando/spec.md` → Servidor na linha de comando | passou | `test_o_servidor_le_host_e_porta` |
| o servidor usa a porta default | `specs/comando/spec.md` → Servidor na linha de comando | passou | `test_o_servidor_usa_a_porta_default` |
| EDGE - argumento desconhecido sai com erro | `specs/comando/spec.md` → Cliente na linha de comando | passou | `test_argumento_desconhecido_sai_com_erro` |

NÃO TESTÁVEL (declarado no qa-plan): `README.md` roteiro de quatro terminais — prosa, leitura manual.

## Evidências

- **Comandos executados:**
  ```bash
  uv run pytest --cov=pysueca --cov-fail-under=80 --cov-report=term-missing -q
  uv run ruff check
  uv run ruff format --check
  uv run mypy src
  ```
- **Saída relevante:** `117 passed`; `All checks passed!`; `65 files already formatted`; `Success: no issues found in 7 source files`; `29 ### Test:` no qa-plan = 29 `def test_` no `tests/test_cliente.py`; `0` tasks desmarcadas.
- **Cobertura:** `TOTAL 98%` (gate 80%): `carta/baralho/motor/protocolo` 100%, `main.py` 97%, `servidor.py` 96%. O retrabalho fechou as linhas `101`, `166/168`, `174-175` e `194` de `main.py`.
- **Ciclo git do retrabalho:** seis commits `test(06-cliente-tui)` com RED demonstrado (reversão temporária do comportamento, diff líquido zero) e `main.py` inalterado.

## Gaps / Tech debt

| O que | Evidência | Criticidade |
|---|---|---|
| `meu_assento` com o nome ausente do snapshot e `enviar` sem conexão não exercitados | `main.py:146,180` descobertas | baixa |
| `main()` do cliente e `main()`/`_servir` do servidor não exercitados (só `analisar`); entrypoint conferido por smoke test manual | `main.py:286-287,291`; `servidor.py:203-205,210-211` | baixa |
| Casos-limite declarados fora de escopo no grill: idempotência de dois `Estado` iguais e `encerrado`/placar final (tela da 07) | ausência de teste | baixa |
| Fora do escopo da 06 (herdado da 05): `Servidor._desconectar` deixa escapar `ConnectionResetError` no `drain` quando um cliente fecha abruptamente | traceback no smoke test, só no fechamento abrupto | baixa |

## Decisão

- **Status:** Aprovado

| O que | Criticidade | Impacto se adiar |
|---|---|---|
| `meu_assento` ausente, `enviar` sem conexão e `main()` das fachadas | baixa | ramos defensivos/fachada; sem caminho de jogo quebrado |
| Idempotência e `encerrado`/placar final | baixa | fora do escopo da 06 (tela final é da 07); a tela é recalculada do snapshot |
| `ConnectionResetError` em `_desconectar` (arrastado da 05) | baixa | cliente TUI fecha de forma limpa; só o fechamento abrupto dispara |

> **Próximo passo:** Aprovado → `LICOES.md` e avançar para `/pi-sprint-propor` (sprint 07).

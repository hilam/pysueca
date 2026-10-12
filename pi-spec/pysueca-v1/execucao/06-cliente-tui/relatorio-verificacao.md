# Relatório de Verificação — Sprint 06-cliente-tui — Cliente TUI — 2026-10-12

> **Sprint:** `sprints/06-cliente-tui/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> **Período:** 2026-10-12

## Cobertura vs qa-plan.md

| Teste | Traces | Status | Evidência |
|---|---|---|---|
| o cliente manda entrar com o nome | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_o_cliente_manda_entrar_com_o_nome` |
| o cliente se reconhece pelo nome | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_o_cliente_se_reconhece_pelo_nome` |
| EDGE - erro do servidor aparece sem derrubar o app | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_erro_do_servidor_aparece_sem_derrubar_o_app` |
| EDGE - mensagem inválida do fio não derruba o app | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_mensagem_invalida_do_fio_nao_derruba_o_app` |
| EDGE - sem servidor o cliente avisa e segue | `specs/cliente/spec.md` → Conexão em worker de tela | passou | `test_sem_servidor_o_cliente_avisa_e_segue` |
| tela de espera mostra N de 4 assentos | `specs/cliente/spec.md` → Espera pela mesa completa | passou | `test_tela_de_espera_mostra_n_de_4_assentos` |
| os assentos mostram a contagem de cartas | `specs/cliente/spec.md` → Espera pela mesa completa | passou | `test_os_assentos_mostram_a_contagem_de_cartas` |
| a mão desenha as cartas com o naipe colorido | `specs/cliente/spec.md` → Mão de cartas em texto | passou | `test_a_mao_desenha_as_cartas_com_o_naipe_colorido` |
| a mesa mostra trunfo, vaza e placar | `specs/cliente/spec.md` → Mão de cartas em texto | passou | `test_a_mesa_mostra_trunfo_vaza_e_placar` |
| ←/→ movem a seleção e Enter joga a carta | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_setas_movem_a_selecao_e_enter_joga_a_carta` |
| EDGE - a seleção não passa dos limites da mão | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_a_selecao_nao_passa_dos_limites_da_mao` |
| EDGE - fora da vez o servidor decide | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_fora_da_vez_o_servidor_decide` |
| EDGE - a seleção volta à primeira carta com a mão nova | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_a_selecao_volta_a_primeira_carta_com_a_mao_nova` |
| EDGE - com a mão vazia nada é jogado | `specs/cliente/spec.md` → Jogada pela seleção | passou | `test_com_a_mao_vazia_nada_e_jogado` |
| cima ou baixo abre na tela do respondente | `specs/cliente/spec.md` → Pergunta cima ou baixo | passou | `test_cima_ou_baixo_abre_na_tela_do_respondente` |
| cima ou baixo responde | `specs/cliente/spec.md` → Pergunta cima ou baixo | passou | `test_cima_ou_baixo_responde` (só `c`; ver Gaps) |
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
- **Saída relevante:** `113 passed`; `All checks passed!`; `64 files already formatted`; `Success: no issues found in 7 source files`.
- **Cobertura:** `TOTAL 97%` (gate 80%): `main.py` 94%, `servidor.py` 96%, `carta/baralho/motor/protocolo` 100%.
- **Smoke test dos entrypoints:** `pysueca --help` e `pysueca-servidor --help` respondem; `pysueca-servidor --porta <efêmera>` subiu e quatro clientes de protocolo sentaram, com `assentos == ["Ana","Bia","Caio","Duda"]` e `respondente == 1`.
- **Ciclo git:** 40+ commits `test(...)`/`feat(...)`/`refactor(...)` com scope `06-cliente-tui`, teste e implementação separados.

## Gaps / Tech debt

| O que | Evidência | Criticidade |
|---|---|---|
| `b` (baixo) sem teste: o requisito "Pergunta cima ou baixo" diz que `b` envia `Responder(False)`, mas o qa-plan/teste só exercita `c` | `main.py:101` descoberta; `grep press("b")` vazio | média |
| Guard de `action_selecionar` com a mão vazia não exercitado (qa-plan só testa `Enter` com mão vazia) | `main.py:194` descoberta | baixa |
| Fim de conexão em pleno jogo (EOF e `finally` do worker) e aviso "Conexão encerrada" não exercitados; o teste "sem servidor" cobre só a falha de `open_connection` | `main.py:166,168,174-175` descobertas | baixa |
| `meu_assento` com o nome ausente do snapshot e `enviar` sem conexão não exercitados | `main.py:146,180` descobertas | baixa |
| `main()` do cliente e `main()`/`_servir` do servidor não exercitados (só `analisar`); entrypoint conferido por smoke test manual | `main.py:286-287,291`; `servidor.py:203-205,210-211` | baixa |
| Casos Limite do qa-plan não testados: vaza vazia e com quatro jogadas, `assentos` com `None` no meio, `encerrado`/placar final, idempotência de dois `Estado` iguais | ausência de teste | baixa |
| Fora do escopo desta sprint: `Servidor._desconectar` deixa escapar `ConnectionResetError` no `drain` quando um cliente fecha abruptamente (pré-existente da 05) | traceback no smoke test, só no fechamento abrupto | baixa |

## Decisão

- **Status:** Aprovado

| O que | Criticidade | Impacto se adiar |
|---|---|---|
| Teste do `b` → `Responder(False)` | média | requisito da spec sem prova; ramo simétrico ao `c`, risco baixo |
| Guard da seleção com mão vazia, EOF/`finally`, nome ausente, `main()` e casos-limite | baixa | ramos defensivos e de fachada; sem caminho de jogo quebrado |
| `ConnectionResetError` em `_desconectar` (arrastado da 05) | baixa | cliente TUI fecha de forma limpa; só o fechamento abrupto dispara |

> **Próximo passo:** Aprovado → `LICOES.md` e avançar para `/pi-sprint-propor` (sprint 07).

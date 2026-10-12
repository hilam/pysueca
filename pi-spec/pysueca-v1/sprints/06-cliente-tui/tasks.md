# Tasks — Sprint 06 — Cliente TUI

> **Sprint:** `sprints/06-cliente-tui/` — rastreia `sprints/06-cliente-tui/qa-plan.md`, `sprints/06-cliente-tui/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [x] 1.1 Criar branch `feat/pysueca-v1-06-cliente-tui` — scope `06-cliente-tui` nos commits
- [x] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 06-cliente-tui — cliente TUI` (`sprints/06-cliente-tui/*.md` + `specs/**`)

## 2. Cliente mínimo: conexão, `entrar` e a tela de espera (tracer bullet, RED → GREEN)

- [x] 2.1 Teste `o cliente manda entrar com o nome` (RED) — em `tests/test_cliente.py`: o `ServidorFalso` (`asyncio.start_server` que desserializa com `protocolo.desserializar` e enfileira numa `asyncio.Queue`) e o helper `rodar(app)` com `asyncio.run(cenario())` + `async with app.run_test() as pilot`
- [x] 2.2 `src/pysueca/main.py` reescrito: `SuecaApp(host, porta, nome)` com o worker `@work(exclusive=True)` que conecta, manda `Entrar(nome)` e lê o laço de linhas traduzindo para `mostrar_estado`/`avisar`; o esqueleto sai inteiro (`PATH_IMAGENS`, `NAIPES`, `CARTAS`, o binding `d` e `action_toggle_dark`, decisão 15) (GREEN)
- [x] 2.3 Commit: `test(06-cliente-tui): o cliente manda entrar com o nome` → `feat(06-cliente-tui): conecta e manda entrar pelo worker de tela`

- [x] 2.4 Teste `tela de espera mostra N de 4 assentos` (RED)
- [x] 2.5 `mostrar_estado` com o painel `#assentos`: `N de 4`, nomes e assentos vagos; guarda o `Estado` corrente e o assento derivado de `assentos.index(nome)` (GREEN)
- [x] 2.6 Commit: `test(06-cliente-tui): tela de espera mostra N de 4 assentos` → `feat(06-cliente-tui): desenha a espera pela mesa completa`

## 3. A mesa desenhada: mão, trunfo, vaza, placar e contagens (RED → GREEN)

- [x] 3.1 Teste `a mão desenha as cartas com o naipe colorido` (RED) — função pura de tela (`desenhar_carta`), sem `App`, cobrindo os quatro naipes e a cor de copas/ouros
- [x] 3.2 `desenhar_carta`/`desenhar_mao` com os símbolos `♣ ♥ ♠ ♦` e o markup de vermelho; o painel `#mao` em uma linha (GREEN)
- [x] 3.3 Commit: `test(06-cliente-tui): a mão desenha as cartas com o naipe colorido` → `feat(06-cliente-tui): desenha a mão em texto colorido`

- [x] 3.4 Teste `a mesa mostra trunfo, vaza e placar` (RED) — agora com a carta do trunfo (`A♥`, de `carta_trunfo`), não só o naipe
- [x] 3.5 Painel `#mesa` com a carta do trunfo, cada carta da vaza junto do assento e as partidas por dupla (GREEN)
- [x] 3.6 Commit: `test(06-cliente-tui): a mesa mostra trunfo, vaza e placar` → `feat(06-cliente-tui): desenha o trunfo, a vaza e o placar`

- [x] 3.7 Teste `os assentos mostram a contagem de cartas` (RED)
- [x] 3.8 `#assentos` com nome e `contagens[i]` de cada assento ocupado (GREEN)
- [x] 3.9 Commit: `test(06-cliente-tui): os assentos mostram a contagem de cartas` → `feat(06-cliente-tui): mostra a contagem de cartas por assento`

## 4. Seleção e jogada de carta (RED → GREEN)

- [x] 4.1 Teste `←/→ movem a seleção e Enter joga a carta` (RED) — `Binding`s de `left`/`right`/`enter` pilotados com `pilot.press` + `pilot.pause`
- [x] 4.2 Índice de seleção com `clamp`, realce no markup e `Enter` mandando `Jogar(carta)` com a carta selecionada (GREEN)
- [x] 4.3 Commit: `test(06-cliente-tui): ←/→ movem a seleção e Enter joga a carta` → `feat(06-cliente-tui): joga a carta selecionada`

- [x] 4.4 Teste `EDGE - a seleção não passa dos limites da mão` (RED)
- [x] 4.5 Guard do `clamp` nas duas pontas (GREEN)
- [x] 4.6 Commit: `test(06-cliente-tui): a seleção não passa dos limites da mão` → `feat(06-cliente-tui): limita a seleção à mão`

- [x] 4.7 Teste `EDGE - fora da vez o servidor decide` (RED) — o cliente manda `Jogar` e mostra o motivo do `erro` devolvido, sem checar a vez
- [x] 4.8 Nenhuma checagem de vez no cliente (GREEN; registrar a asserção do motivo recebido)
- [x] 4.9 Commit: `test(06-cliente-tui): fora da vez o servidor decide` → `feat(06-cliente-tui): deixa a regra da vez com o servidor`

- [x] 4.10 Teste `EDGE - a seleção volta à primeira carta com a mão nova` (RED)
- [x] 4.11 `mostrar_estado` zera a seleção quando a mão muda (GREEN)
- [x] 4.12 Commit: `test(06-cliente-tui): a seleção volta à primeira carta com a mão nova` → `feat(06-cliente-tui): reinicia a seleção a cada mão`

- [x] 4.13 Teste `EDGE - com a mão vazia nada é jogado` (RED esperado verde — é o guard do `clamp`/mão vazia de 4.5; registrar como cobertura)
- [x] 4.14 Nenhuma implementação nova (GREEN)
- [x] 4.15 Commit: `test(06-cliente-tui): com a mão vazia nada é jogado`

## 5. Pergunta cima ou baixo (RED → GREEN)

- [x] 5.1 Teste `cima ou baixo abre na tela do respondente` (RED) — `ModalScreen` empilhado quando `trunfo is None` e `respondente == meu_assento`
- [x] 5.2 `RespostaScreen(ModalScreen)` com as duas respostas e a condição de abertura em `mostrar_estado` (GREEN)
- [x] 5.3 Commit: `test(06-cliente-tui): cima ou baixo abre na tela do respondente` → `feat(06-cliente-tui): abre o diálogo do respondente`

- [x] 5.4 Teste `cima ou baixo responde` (RED) — `Binding` de `c`/`b` mandando `Responder(True/False)` e fechando o modal
- [x] 5.5 Ações do modal chamando `enviar(Responder(...))` e `pop_screen` (GREEN)
- [x] 5.6 Commit: `test(06-cliente-tui): cima ou baixo responde` → `feat(06-cliente-tui): responde cima ou baixo`

- [x] 5.7 Teste `EDGE - quem não é o respondente não vê o diálogo` (RED) — `respondente` em outro assento; e o modal aberto fecha no snapshot com o trunfo preparado
- [x] 5.8 Fechamento do modal quando a pergunta deixa de ser do jogador (GREEN)
- [x] 5.9 Commit: `test(06-cliente-tui): quem não é o respondente não vê o diálogo` → `feat(06-cliente-tui): fecha o diálogo quando a pergunta passa`

## 6. Queda, conexão e erro (RED → GREEN)

- [x] 6.1 Teste `a queda aparece na tela` (RED) — `ausentes == [2]` no painel `#aviso` com o nome do assento
- [x] 6.2 Prioridade do `#aviso` (ausentes > vez > conectando) com o nome do assento ausente (GREEN)
- [x] 6.3 Commit: `test(06-cliente-tui): a queda aparece na tela` → `feat(06-cliente-tui): avisa a mesa congelada`

- [x] 6.4 Teste `EDGE - reconexão limpa a tela de queda` (RED)
- [x] 6.5 Aviso derivado do snapshot a cada evento, sem estado acumulado (GREEN)
- [x] 6.6 Commit: `test(06-cliente-tui): reconexão limpa a tela de queda` → `feat(06-cliente-tui): limpa o aviso quando a mesa volta`

- [x] 6.7 Teste `EDGE - erro do servidor aparece sem derrubar o app` (RED)
- [x] 6.8 `avisar(motivo)` para o `Erro` recebido, mantendo o laço de leitura vivo (GREEN)
- [x] 6.9 Commit: `test(06-cliente-tui): erro do servidor aparece sem derrubar o app` → `feat(06-cliente-tui): mostra o motivo do erro na tela`

- [x] 6.10 Teste `EDGE - mensagem inválida do fio não derruba o app` (RED esperado verde — mesmo ramo de 6.8; registrar como cobertura)
- [x] 6.11 Nenhuma implementação nova (GREEN)
- [x] 6.12 Commit: `test(06-cliente-tui): mensagem inválida do fio não derruba o app`

- [x] 6.13 Teste `EDGE - sem servidor o cliente avisa e segue` (RED) — porta fechada e `OSError` no `open_connection`
- [x] 6.14 `try/except OSError` no worker virando aviso, e o `finally` único do laço (fim de conexão, teto do leitor e reset no mesmo caminho) (GREEN)
- [x] 6.15 Commit: `test(06-cliente-tui): sem servidor o cliente avisa e segue` → `feat(06-cliente-tui): trata a falha de conexão como aviso`

- [x] 6.16 Teste `o cliente se reconhece pelo nome` (RED) — `assentos == ["Bia", "Ana", None, None]` e `vez == 1` mostrando a vez como do jogador
- [x] 6.17 `meu_assento` derivado de `assentos.index(nome)` alimentando vez e respondente (GREEN)
- [x] 6.18 Commit: `test(06-cliente-tui): o cliente se reconhece pelo nome` → `feat(06-cliente-tui): deriva o assento do próprio nome`

- [x] 6.19 Teste `EDGE - congelado o cliente ainda manda e o servidor recusa` (RED esperado verde — o envio sem guard de 4.2 e o aviso de 6.8 já cobrem; registrar como cobertura da decisão 4 do grill)
- [x] 6.20 Nenhuma implementação nova (GREEN)
- [x] 6.21 Commit: `test(06-cliente-tui): congelado o cliente ainda manda e o servidor recusa`

## 7. Linha de comando e roteiro de quatro terminais (RED → GREEN)

- [x] 7.1 Teste `o cliente lê nome, host e porta` e `o cliente usa os defaults` (RED) — parsing puro do `main(argv)` do `main.py`, sem subir a tela
- [x] 7.2 `main(argv)` do cliente com `argparse`: nome posicional obrigatório, `--host` e `--porta` com defaults `127.0.0.1`/`8765` (GREEN)
- [x] 7.3 Commit: `test(06-cliente-tui): o cliente lê nome, host e porta` → `feat(06-cliente-tui): sobe o cliente por linha de comando`

- [x] 7.4 Teste `o servidor lê host e porta` e `o servidor usa a porta default` (RED) — parsing do `main(argv)` novo do `servidor.py`
- [x] 7.5 `main(argv)` no `servidor.py` com `argparse` e `asyncio.run` sobre `Servidor.iniciar` (GREEN)
- [x] 7.6 `pyproject.toml:12`: `pysueca = "pysueca.main:main"` e `pysueca-servidor = "pysueca.servidor:main"` (GREEN)
- [x] 7.7 Commit: `test(06-cliente-tui): o servidor lê host e porta` → `feat(06-cliente-tui): sobe o servidor por linha de comando e corrige o entrypoint`

- [x] 7.8 Teste `EDGE - argumento desconhecido sai com erro` (RED)
- [x] 7.9 Nenhuma guarda extra: o `argparse` já termina com `SystemExit` (GREEN; asserção de código de saída)
- [x] 7.10 Commit: `test(06-cliente-tui): argumento desconhecido sai com erro` → `feat(06-cliente-tui): recusa argumento desconhecido`

- [x] 7.11 `README.md:56`: roteiro manual de 4 terminais (servidor + quatro clientes com nomes) e a nota de que a ordem de conexão define os assentos e as duplas 0–2 e 1–3 (GREEN)
- [x] 7.12 Commit: `docs(06-cliente-tui): roteiro manual de quatro terminais`

## 8. Refatoração (apenas no GREEN)

- [x] 8.1 Refatorar `main.py` mantendo todos os testes verdes (ex.: separar o render de cada painel do `mostrar_estado`, tirar do worker qualquer decisão de tela)
- [x] 8.2 Rodar a suite completa
- [x] 8.3 Commit: `refactor(06-cliente-tui): isola o render dos painéis do worker`

## 9. Documentação

- [x] 9.1 `AGENTS.md`: `src/pysueca/main.py` como o cliente Textual (worker de fio, painéis, teclas) e a invariante de que nenhum widget conhece o protocolo; a linha do `pyproject.toml:12` deixa de ser dívida
- [x] 9.2 Commit: `docs(06-cliente-tui): documenta o cliente e a fronteira widget/protocolo`

## 10. Validação Final

- [x] 10.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [x] 10.2 Tipos: `uv run mypy src` (o erro pré-existente do `main.py:52` fecha nesta sprint)
- [x] 10.3 Suite completa uma última vez: `uv run pytest`
- [x] 10.4 Gate de cobertura: `uv run pytest --cov=pysueca --cov-fail-under=80`
- [x] 10.5 Roteiro manual de 4 terminais conferido à mão (servidor + quatro clientes, uma mão completa)
- [x] 10.6 Commit de ajustes finais: `style: aplica lint e formatação`

## 11. Retrabalho da verificação (RED → GREEN)

- [x] 11.1 Ampliar o teste `cima ou baixo responde` com o ramo `b` → `Responder(False)` (RED — Test: cima ou baixo responde)
- [x] 11.2 Nenhuma implementação nova: `RespostaScreen.action_baixo` já existe (GREEN; cobertura declarada)
- [x] 11.3 Commit: `test(06-cliente-tui): cima ou baixo responde com o baixo`

- [x] 11.4 Teste `EDGE - o fim da conexão vira aviso` (RED) — o falso fecha a conexão e a tela avisa
- [x] 11.5 Nenhuma implementação nova: o `finally` do worker já avisa sob `is_running` (GREEN; cobertura declarada)
- [x] 11.6 Commit: `test(06-cliente-tui): o fim da conexão vira aviso`

- [x] 11.7 Teste `EDGE - o teto do leitor vira aviso` (RED) — linha maior que `LIMITE_LEITURA`
- [x] 11.8 Nenhuma implementação nova: o `except (ValueError, LinhaLonga)` converge no `finally` (GREEN; cobertura declarada)
- [x] 11.9 Commit: `test(06-cliente-tui): o teto do leitor vira aviso`

- [x] 11.10 Teste `a mesa desenha a vaza vazia e a vaza cheia` (RED) — helper puro `desenhar_mesa`
- [x] 11.11 Nenhuma implementação nova (GREEN; cobertura declarada)
- [x] 11.12 Commit: `test(06-cliente-tui): a mesa desenha a vaza vazia e a vaza cheia`

- [x] 11.13 Teste `os assentos contam os nomes com um assento vago no meio` (RED) — helper puro `desenhar_assentos`
- [x] 11.14 Nenhuma implementação nova (GREEN; cobertura declarada)
- [x] 11.15 Commit: `test(06-cliente-tui): os assentos contam os nomes com um assento vago no meio`

- [x] 11.16 Ampliar `com a mão vazia nada é jogado`: `←`/`→` mantêm a seleção em 0 (RED)
- [x] 11.17 Nenhuma implementação nova: `action_selecionar` já guarda `not self.estado.mao` (GREEN; cobertura declarada)
- [x] 11.18 Commit: `test(06-cliente-tui): a seleção fica em 0 com a mão vazia`

- [x] 11.19 Rodar a suite completa e o gate de cobertura (`uv run pytest --cov=pysueca --cov-fail-under=80`)

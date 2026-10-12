# Tasks — Sprint 06 — Cliente TUI

> **Sprint:** `sprints/06-cliente-tui/` — rastreia `sprints/06-cliente-tui/qa-plan.md`, `sprints/06-cliente-tui/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [ ] 1.1 Criar branch `feat/pysueca-v1-06-cliente-tui` — scope `06-cliente-tui` nos commits
- [ ] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 06-cliente-tui — cliente TUI` (`sprints/06-cliente-tui/*.md` + `specs/**`)

## 2. Cliente mínimo: conexão, `entrar` e a tela de espera (tracer bullet, RED → GREEN)

- [ ] 2.1 Teste `o cliente manda entrar com o nome` (RED) — em `tests/test_cliente.py`: o `ServidorFalso` (`asyncio.start_server` que desserializa com `protocolo.desserializar` e enfileira numa `asyncio.Queue`) e o helper `rodar(app)` com `asyncio.run(cenario())` + `async with app.run_test() as pilot`
- [ ] 2.2 `src/pysueca/main.py` reescrito: `SuecaApp(host, porta, nome)` com o worker `@work(exclusive=True)` que conecta, manda `Entrar(nome)` e lê o laço de linhas traduzindo para `mostrar_estado`/`avisar`; o esqueleto sai inteiro (`PATH_IMAGENS`, `NAIPES`, `CARTAS`, o binding `d` e `action_toggle_dark`, decisão 15) (GREEN)
- [ ] 2.3 Commit: `test(06-cliente-tui): o cliente manda entrar com o nome` → `feat(06-cliente-tui): conecta e manda entrar pelo worker de tela`

- [ ] 2.4 Teste `tela de espera mostra N de 4 assentos` (RED)
- [ ] 2.5 `mostrar_estado` com o painel `#assentos`: `N de 4`, nomes e assentos vagos; guarda o `Estado` corrente e o assento derivado de `assentos.index(nome)` (GREEN)
- [ ] 2.6 Commit: `test(06-cliente-tui): tela de espera mostra N de 4 assentos` → `feat(06-cliente-tui): desenha a espera pela mesa completa`

## 3. A mesa desenhada: mão, trunfo, vaza, placar e contagens (RED → GREEN)

- [ ] 3.1 Teste `a mão desenha as cartas com o naipe colorido` (RED) — função pura de tela (`desenhar_carta`), sem `App`, cobrindo os quatro naipes e a cor de copas/ouros
- [ ] 3.2 `desenhar_carta`/`desenhar_mao` com os símbolos `♣ ♥ ♠ ♦` e o markup de vermelho; o painel `#mao` em uma linha (GREEN)
- [ ] 3.3 Commit: `test(06-cliente-tui): a mão desenha as cartas com o naipe colorido` → `feat(06-cliente-tui): desenha a mão em texto colorido`

- [ ] 3.4 Teste `a mesa mostra trunfo, vaza e placar` (RED) — agora com a carta do trunfo (`A♥`, de `carta_trunfo`), não só o naipe
- [ ] 3.5 Painel `#mesa` com a carta do trunfo, cada carta da vaza junto do assento e as partidas por dupla (GREEN)
- [ ] 3.6 Commit: `test(06-cliente-tui): a mesa mostra trunfo, vaza e placar` → `feat(06-cliente-tui): desenha o trunfo, a vaza e o placar`

- [ ] 3.7 Teste `os assentos mostram a contagem de cartas` (RED)
- [ ] 3.8 `#assentos` com nome e `contagens[i]` de cada assento ocupado (GREEN)
- [ ] 3.9 Commit: `test(06-cliente-tui): os assentos mostram a contagem de cartas` → `feat(06-cliente-tui): mostra a contagem de cartas por assento`

## 4. Seleção e jogada de carta (RED → GREEN)

- [ ] 4.1 Teste `←/→ movem a seleção e Enter joga a carta` (RED) — `Binding`s de `left`/`right`/`enter` pilotados com `pilot.press` + `pilot.pause`
- [ ] 4.2 Índice de seleção com `clamp`, realce no markup e `Enter` mandando `Jogar(carta)` com a carta selecionada (GREEN)
- [ ] 4.3 Commit: `test(06-cliente-tui): ←/→ movem a seleção e Enter joga a carta` → `feat(06-cliente-tui): joga a carta selecionada`

- [ ] 4.4 Teste `EDGE - a seleção não passa dos limites da mão` (RED)
- [ ] 4.5 Guard do `clamp` nas duas pontas (GREEN)
- [ ] 4.6 Commit: `test(06-cliente-tui): a seleção não passa dos limites da mão` → `feat(06-cliente-tui): limita a seleção à mão`

- [ ] 4.7 Teste `EDGE - fora da vez o servidor decide` (RED) — o cliente manda `Jogar` e mostra o motivo do `erro` devolvido, sem checar a vez
- [ ] 4.8 Nenhuma checagem de vez no cliente (GREEN; registrar a asserção do motivo recebido)
- [ ] 4.9 Commit: `test(06-cliente-tui): fora da vez o servidor decide` → `feat(06-cliente-tui): deixa a regra da vez com o servidor`

- [ ] 4.10 Teste `EDGE - a seleção volta à primeira carta com a mão nova` (RED)
- [ ] 4.11 `mostrar_estado` zera a seleção quando a mão muda (GREEN)
- [ ] 4.12 Commit: `test(06-cliente-tui): a seleção volta à primeira carta com a mão nova` → `feat(06-cliente-tui): reinicia a seleção a cada mão`

- [ ] 4.13 Teste `EDGE - com a mão vazia nada é jogado` (RED esperado verde — é o guard do `clamp`/mão vazia de 4.5; registrar como cobertura)
- [ ] 4.14 Nenhuma implementação nova (GREEN)
- [ ] 4.15 Commit: `test(06-cliente-tui): com a mão vazia nada é jogado`

## 5. Pergunta cima ou baixo (RED → GREEN)

- [ ] 5.1 Teste `cima ou baixo abre na tela do respondente` (RED) — `ModalScreen` empilhado quando `trunfo is None` e `respondente == meu_assento`
- [ ] 5.2 `RespostaScreen(ModalScreen)` com as duas respostas e a condição de abertura em `mostrar_estado` (GREEN)
- [ ] 5.3 Commit: `test(06-cliente-tui): cima ou baixo abre na tela do respondente` → `feat(06-cliente-tui): abre o diálogo do respondente`

- [ ] 5.4 Teste `cima ou baixo responde` (RED) — `Binding` de `c`/`b` mandando `Responder(True/False)` e fechando o modal
- [ ] 5.5 Ações do modal chamando `enviar(Responder(...))` e `pop_screen` (GREEN)
- [ ] 5.6 Commit: `test(06-cliente-tui): cima ou baixo responde` → `feat(06-cliente-tui): responde cima ou baixo`

- [ ] 5.7 Teste `EDGE - quem não é o respondente não vê o diálogo` (RED) — `respondente` em outro assento; e o modal aberto fecha no snapshot com o trunfo preparado
- [ ] 5.8 Fechamento do modal quando a pergunta deixa de ser do jogador (GREEN)
- [ ] 5.9 Commit: `test(06-cliente-tui): quem não é o respondente não vê o diálogo` → `feat(06-cliente-tui): fecha o diálogo quando a pergunta passa`

## 6. Queda, conexão e erro (RED → GREEN)

- [ ] 6.1 Teste `a queda aparece na tela` (RED) — `ausentes == [2]` no painel `#aviso` com o nome do assento
- [ ] 6.2 Prioridade do `#aviso` (ausentes > vez > conectando) com o nome do assento ausente (GREEN)
- [ ] 6.3 Commit: `test(06-cliente-tui): a queda aparece na tela` → `feat(06-cliente-tui): avisa a mesa congelada`

- [ ] 6.4 Teste `EDGE - reconexão limpa a tela de queda` (RED)
- [ ] 6.5 Aviso derivado do snapshot a cada evento, sem estado acumulado (GREEN)
- [ ] 6.6 Commit: `test(06-cliente-tui): reconexão limpa a tela de queda` → `feat(06-cliente-tui): limpa o aviso quando a mesa volta`

- [ ] 6.7 Teste `EDGE - erro do servidor aparece sem derrubar o app` (RED)
- [ ] 6.8 `avisar(motivo)` para o `Erro` recebido, mantendo o laço de leitura vivo (GREEN)
- [ ] 6.9 Commit: `test(06-cliente-tui): erro do servidor aparece sem derrubar o app` → `feat(06-cliente-tui): mostra o motivo do erro na tela`

- [ ] 6.10 Teste `EDGE - mensagem inválida do fio não derruba o app` (RED esperado verde — mesmo ramo de 6.8; registrar como cobertura)
- [ ] 6.11 Nenhuma implementação nova (GREEN)
- [ ] 6.12 Commit: `test(06-cliente-tui): mensagem inválida do fio não derruba o app`

- [ ] 6.13 Teste `EDGE - sem servidor o cliente avisa e segue` (RED) — porta fechada e `OSError` no `open_connection`
- [ ] 6.14 `try/except OSError` no worker virando aviso, e o `finally` único do laço (fim de conexão, teto do leitor e reset no mesmo caminho) (GREEN)
- [ ] 6.15 Commit: `test(06-cliente-tui): sem servidor o cliente avisa e segue` → `feat(06-cliente-tui): trata a falha de conexão como aviso`

- [ ] 6.16 Teste `o cliente se reconhece pelo nome` (RED) — `assentos == ["Bia", "Ana", None, None]` e `vez == 1` mostrando a vez como do jogador
- [ ] 6.17 `meu_assento` derivado de `assentos.index(nome)` alimentando vez e respondente (GREEN)
- [ ] 6.18 Commit: `test(06-cliente-tui): o cliente se reconhece pelo nome` → `feat(06-cliente-tui): deriva o assento do próprio nome`

- [ ] 6.19 Teste `EDGE - congelado o cliente ainda manda e o servidor recusa` (RED esperado verde — o envio sem guard de 4.2 e o aviso de 6.8 já cobrem; registrar como cobertura da decisão 4 do grill)
- [ ] 6.20 Nenhuma implementação nova (GREEN)
- [ ] 6.21 Commit: `test(06-cliente-tui): congelado o cliente ainda manda e o servidor recusa`

## 7. Linha de comando e roteiro de quatro terminais (RED → GREEN)

- [ ] 7.1 Teste `o cliente lê nome, host e porta` e `o cliente usa os defaults` (RED) — parsing puro do `main(argv)` do `main.py`, sem subir a tela
- [ ] 7.2 `main(argv)` do cliente com `argparse`: nome posicional obrigatório, `--host` e `--porta` com defaults `127.0.0.1`/`8765` (GREEN)
- [ ] 7.3 Commit: `test(06-cliente-tui): o cliente lê nome, host e porta` → `feat(06-cliente-tui): sobe o cliente por linha de comando`

- [ ] 7.4 Teste `o servidor lê host e porta` e `o servidor usa a porta default` (RED) — parsing do `main(argv)` novo do `servidor.py`
- [ ] 7.5 `main(argv)` no `servidor.py` com `argparse` e `asyncio.run` sobre `Servidor.iniciar` (GREEN)
- [ ] 7.6 `pyproject.toml:12`: `pysueca = "pysueca.main:main"` e `pysueca-servidor = "pysueca.servidor:main"` (GREEN)
- [ ] 7.7 Commit: `test(06-cliente-tui): o servidor lê host e porta` → `feat(06-cliente-tui): sobe o servidor por linha de comando e corrige o entrypoint`

- [ ] 7.8 Teste `EDGE - argumento desconhecido sai com erro` (RED)
- [ ] 7.9 Nenhuma guarda extra: o `argparse` já termina com `SystemExit` (GREEN; asserção de código de saída)
- [ ] 7.10 Commit: `test(06-cliente-tui): argumento desconhecido sai com erro` → `feat(06-cliente-tui): recusa argumento desconhecido`

- [ ] 7.11 `README.md:56`: roteiro manual de 4 terminais (servidor + quatro clientes com nomes) e a nota de que a ordem de conexão define os assentos e as duplas 0–2 e 1–3 (GREEN)
- [ ] 7.12 Commit: `docs(06-cliente-tui): roteiro manual de quatro terminais`

## 8. Refatoração (apenas no GREEN)

- [ ] 8.1 Refatorar `main.py` mantendo todos os testes verdes (ex.: separar o render de cada painel do `mostrar_estado`, tirar do worker qualquer decisão de tela)
- [ ] 8.2 Rodar a suite completa
- [ ] 8.3 Commit: `refactor(06-cliente-tui): isola o render dos painéis do worker`

## 9. Documentação

- [ ] 9.1 `AGENTS.md`: `src/pysueca/main.py` como o cliente Textual (worker de fio, painéis, teclas) e a invariante de que nenhum widget conhece o protocolo; a linha do `pyproject.toml:12` deixa de ser dívida
- [ ] 9.2 Commit: `docs(06-cliente-tui): documenta o cliente e a fronteira widget/protocolo`

## 10. Validação Final

- [ ] 10.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [ ] 10.2 Tipos: `uv run mypy src` (o erro pré-existente do `main.py:52` fecha nesta sprint)
- [ ] 10.3 Suite completa uma última vez: `uv run pytest`
- [ ] 10.4 Gate de cobertura: `uv run pytest --cov=pysueca --cov-fail-under=80`
- [ ] 10.5 Roteiro manual de 4 terminais conferido à mão (servidor + quatro clientes, uma mão completa)
- [ ] 10.6 Commit de ajustes finais: `style: aplica lint e formatação`

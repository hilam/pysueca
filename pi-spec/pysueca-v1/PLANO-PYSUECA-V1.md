# Plano de Sprints — PYSUECA-V1

## Visão geral

Uma mesa de Sueca para quatro jogadores em terminais diferentes: um servidor headless dono das regras, quatro clientes Textual que mandam intenções e desenham o estado que recebem. O motor de regras é puro e síncrono (sem `asyncio`, sem Textual), a rede é TCP com JSON de uma linha e snapshot completo, e o harness de teste é 4 clientes + 1 servidor em `localhost` — não existe modo hot-seat. Vocabulário em `CONTEXT.md`, regras em `README.md`, decisões em `docs/adr/0001`–`0005`.

**Feito até agora:** esqueleto Textual em `src/pysueca/main.py` (57 linhas, substituído na sprint 06), 40 PNGs sem uso em `src/pysueca/imagens/`, `pyproject.toml` com Textual e dev-tools (pytest, ruff, mypy, bandit) e duas entrypoints, uma delas quebrada (`pyproject.toml:12`). Não existe `tests/`, `AGENTS.md` nem código de regra.

---

## Sprint 01 — Carta e baralho

**Objetivo:** representar as 40 cartas de Sueca com pontos e força corretos.

**Decisão arquitetural:** separar `carta.py` de `motor.py` — a aritmética de carta (força, pontos, `de_texto`) é usada pelo motor e pelo protocolo, e é o único lugar que sabe a ordem `A > 7 > K > J > Q > 6 > 5 > 4 > 3 > 2`, que **não** é a ordem de pontos. O **RNG é injetado**: `Baralho`, `Mao` e `Jogo` recebem um `random.Random` com default próprio, nunca o `random` global, para que os testes testem um cenário concreto ("o assento 2 ficou com o Ás de trunfo") e não apenas invariantes. Detalhada em `sprints/01-carta-e-baralho/design.md`; ver `docs/adr/0004`.

**Entregável:** `tests/test_carta.py` verde, provando que o baralho tem 40 cartas, que os pontos somam 120, que o Ás de trunfo vence qualquer carta e que `"7H"` ida-e-volta preserva naipe e valor; mais `AGENTS.md` criado (comandos `uv run`, mapa de arquivos, as invariantes "motor puro e síncrono" e "só Textual", ponteiro para `docs/adr/`). Todos os testes verdes.

**Riscos desta sprint:** N/A

---

## Sprint 02 — Vaza e mão

**Objetivo:** jogar uma mão completa no motor, sem rede e sem UI.

**Decisão arquitetural:** `Mao` como máquina de estados explícita (`preparar` → 10 vazas → `pontuar`), com `Mao.jogar` devolvendo erro em vez de exceção para jogada ilegal — o servidor não pode derrubar a mesa por causa de um cliente. A `Mao` usa o RNG injetado na sprint 01, então toda vaza testada tem seed determinística. Ver `CONTEXT.md` (Vaza, Puxar, Trunfar, Mão) e `sprints/02-vaza-e-mao/design.md`.

**Entregável:** `tests/test_motor.py` verde, jogando uma mão inteira com 4 jogadores escolhendo cartas legais ao acaso e provando: naipe puxado é obrigatório, trunfo vence naipe, entre trunfos vence a maior, quem levou puxa a seguinte, e o resultado (bandeira/quilo/normal/empate) sai dos limites de `README.md`. Todos os testes verdes.

**Riscos desta sprint:** a distribuição "cima/baixo" só é observável por quem fica com a carta do trunfo. Mitigação: modelo reduzido do `docs/adr/0003` — `trunfo = baralho.pop(0 ou -1)` e o resto é sorteio, sem modelar a ordem da distribuição.

---

## Sprint 03 — Jogo e papéis

**Objetivo:** a corrida até 4 partidas, com rotação de papéis e placar.

**Decisão arquitetural:** `Jogo` acumula partidas por dupla e encerra ao chegar a 4 partidas (a bandeira, que vale 4, cai nessa regra); a rotação de embaralhador/cortador/dador anda um assento por mão. Ver `README.md` item 10 da Dinâmica e `sprints/03-jogo-e-papeis/design.md`.

**Entregável:** `tests/test_jogo.py` verde, provando que o embaralhador puxa a primeira vaza, que os papéis rotacionam um assento por mão, que bandeira encerra o jogo na hora, que uma mão de 60 a 60 não dá partida a ninguém e que o jogo acaba ao chegar a 4 partidas. Todos os testes verdes.

**Riscos desta sprint:** N/A

---

## Sprint 04 — Protocolo

**Objetivo:** serializar e desserializar as mensagens sem nenhuma rede.

**Decisão arquitetural:** uma linha JSON por mensagem, com snapshot `estado` completo a cada evento (`docs/adr/0002`), e **validação estrita** no `protocolo.py`, usada pelos dois lados: teto de bytes por linha — único caso que fecha a conexão, porque `readline()` sem limite é DoS de memória —, tipo desconhecido ou campo faltando vira `erro`, `jogar` fora da vez ou com carta que não está na mão do assento vira `erro`, e o nome é normalizado (`strip`, 1 a 20 caracteres) antes de virar identidade. Só a violação de tamanho é fatal; o resto é erro recuperável e a mesa segue. Detalhada em `sprints/04-protocolo/design.md`.

**Entregável:** `tests/test_protocolo.py` verde, provando ida-e-volta de `entrar`/`responder`/`jogar`/`estado`, que o snapshot de um assento traz a própria mão e apenas a **contagem** das outras, e que mensagem ruim não derruba nada: linha malformada, tipo desconhecido, campo faltando, carta ausente da mão e jogada fora da vez viram `erro` tratado, enquanto linha acima do teto de bytes fecha a conexão. Todos os testes verdes.

**Riscos desta sprint:** a validação de rede soma trabalho e 1 dia (P) fica apertado. Mitigação: manter P e cortar por último os testes de caso de borda menos prováveis (nome com 20 caracteres), nunca a validação em si.

---

## Sprint 05 — Servidor

**Objetivo:** quatro clientes de teste jogam uma mão inteira contra o servidor por TCP em `localhost`.

**Decisão arquitetural:** o servidor é a única casca `asyncio`, valida intenções chamando `motor.py` e transmite snapshots — `docs/adr/0001`. Queda de conexão congela a mesa e reserva o assento, sem timer — `docs/adr/0005`. Ver `sprints/05-servidor/design.md`.

**Entregável:** `tests/test_servidor.py` verde, com 4 conexões `asyncio` concorrentes (clientes-robô que jogam legalmente ao acaso) levando uma mão até a contagem, mais reconexão com o mesmo nome retomando o assento, recusa de nome já sentado, e linha acima do teto fechando **aquela** conexão sem derrubar a mesa. Este é o harness que substitui os 4 terminais. Todos os testes verdes.

**Riscos desta sprint:** o congelamento da mesa pode virar ponto morto no teste. Mitigação: timeout curto no teste e asserção explícita de que a mensagem de queda chegou aos outros três.

---

## Sprint 06 — Cliente TUI

**Objetivo:** 4 `pysueca` em 4 terminais jogam uma mão completa contra o servidor.

**Decisão arquitetural:** a leitura do socket é um worker asyncio do Textual que só traduz mensagem em método de tela; nenhum widget conhece o protocolo. Cartas em texto com naipe colorido — `docs/adr/0004`. Ver `sprints/06-cliente-tui/design.md`.

**Entregável:** `tests/test_cliente.py` verde com `App.run_test()` e um servidor falso, cobrindo a tela de espera (N de 4 assentos ocupados, antes de a mesa começar), a seleção de carta com `←`/`→`/`Enter`, o diálogo de "cima ou baixo" na tela do parceiro do dador e a tela de queda; mais o roteiro manual de 4 terminais documentado no `README.md`. Todos os testes verdes.

**Riscos desta sprint:** `80x24` apertado para 4 assentos + 10 cartas. Mitigação: mão em uma linha de ~20 colunas, assentos com a carta da vaza, placar no Header.

---

## Sprint 07 — Polimento

**Objetivo:** a mesa é jogável por pessoas que não escreveram o código.

**Decisão arquitetural:** N/A — ver `sprints/07-polimento/design.md`.

**Entregável:** mensagens de erro do servidor visíveis na tela, placar final do jogo, `d` relica o dark/light existente, teclas no Footer, e `README.md` fechado com o pronto do v1 (quatro pessoas em máquinas diferentes jogam uma série até 4 partidas) e o passo a passo de jogar entre duas máquinas (bind da porta). Todos os testes verdes.

**Riscos desta sprint:** N/A

---

## Dependências

```
01 ─→ 02 ─→ 03 ─→ 04 ─┬─→ 05 ─→ 06 ─→ 07
                       └┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈→ 06
```

Sprints paralelizáveis: **06** pode iniciar logo após **04**, desenvolvendo os widgets contra um servidor falso; a integração real depende de **05**. As sprints 01–04 são estritamente sequenciais.

## Ciclo TDD por feature

Cada tarefa segue **Red** (teste mínimo que falha) → **Green** (implementação mais simples que passa) → **Refactor** (limpar sem quebrar os testes). `uv run pytest` a cada commit, mais `uv run ruff check` e `uv run mypy src`. O motor (01–03) é testado sem rede e sem UI; o protocolo (04) sem rede; só 05 e 06 tocam `asyncio`, e a prova final de 05 é uma mão inteira por TCP.

## Estimativa

| Sprint | Esforço | Dias |
|---|---|---|
| 01 — Carta e baralho | P | 1 |
| 02 — Vaza e mão | M | 3 |
| 03 — Jogo e papéis | P | 1 |
| 04 — Protocolo | P | 1 |
| 05 — Servidor | M | 3 |
| 06 — Cliente TUI | M | 3 |
| 07 — Polimento | P | 1 |

**Total:** ~13 dias para 1 dev.

## Riscos globais

| Risco | Mitigação |
|---|---|
| Regra ainda ambígua na hora de codar | `README.md` e `CONTEXT.md` são canônicos; divergência vira pergunta, não decisão silenciosa |
| Cliente Textual e asyncio brigando | o socket nunca toca widget: o worker traduz para mensagem de tela |
| Ninguém entende o `estado` ao debugar | JSON de uma linha: `nc localhost 8765` mostra a conversa inteira |
| Sem TLS nem autenticação | aceitável em `localhost` e rede local; fora disso, é outro ADR |

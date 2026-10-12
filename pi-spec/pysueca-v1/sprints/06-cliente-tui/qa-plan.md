# QA Plan — Sprint 06 — Cliente TUI

> **Sprint:** `sprints/06-cliente-tui/` — rastreia `sprints/06-cliente-tui/specs/<capability>/spec.md`

## Capability: cliente

### Test: o cliente manda entrar com o nome
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — CRITICAL
- **GIVEN** um servidor falso roteirizado escutando em `127.0.0.1` na porta efêmera
- **WHEN** o `SuecaApp(host, porta, "Ana")` roda dentro de `App.run_test()` e conecta
- **THEN** a primeira linha que o falso recebe é `entrar` com o nome `"Ana"` (desserializada com `protocolo.desserializar`, não comparada como string crua)

### Test: o cliente se reconhece pelo nome
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — CRITICAL
- **GIVEN** o cliente `"Ana"` conectado e o snapshot com `assentos == ["Bia", "Ana", None, None]` e `vez == 1`
- **THEN** a tela mostra a vez como sendo do jogador, provando que o assento saiu de `assentos.index("Ana")` e não de um campo que o snapshot não tem

### Test: EDGE - erro do servidor aparece sem derrubar o app
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — EDGE
- **GIVEN** um cliente sentado com a tela de espera desenhada
- **WHEN** o falso manda `erro` com motivo `nome_em_uso`
- **THEN** a tela mostra `nome_em_uso` no aviso e o app segue de pé, ainda lendo o fio (o falso manda um `estado` depois e a tela muda)

### Test: EDGE - mensagem inválida do fio não derruba o app
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — EDGE
- **GIVEN** um cliente conectado
- **WHEN** o falso manda uma linha que não é JSON
- **THEN** a tela mostra um aviso e o app segue de pé — o ramo é o mesmo do `erro` acima (cobertura: registrar como EDGE, não como RED independente)

### Test: EDGE - sem servidor o cliente avisa e segue
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — EDGE
- **GIVEN** nenhum servidor escutando em `127.0.0.1` na porta escolhida
- **WHEN** o cliente tenta conectar dentro do `run_test`
- **THEN** a tela mostra o aviso de conexão, o app segue de pé e nenhuma exceção escapa ao loop

### Test: EDGE - o fim da conexão vira aviso
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — EDGE
- **GIVEN** o cliente `"Ana"` sentado e a tela de espera desenhada
- **WHEN** o falso fecha a conexão
- **THEN** a tela mostra o aviso de conexão encerrada e o app segue de pé, sem exceção no loop

### Test: EDGE - o teto do leitor vira aviso
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — EDGE
- **GIVEN** o cliente `"Ana"` conectado
- **WHEN** o falso manda uma linha maior que o `LIMITE_LEITURA` do cliente
- **THEN** a tela mostra o aviso de conexão encerrada e o app segue de pé — o `except (ValueError, LinhaLonga)` converge no mesmo `finally` (decisão 10)

### Test: tela de espera mostra N de 4 assentos
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Espera pela mesa completa — CRITICAL
- **GIVEN** o cliente `"Ana"` conectado
- **WHEN** o snapshot traz `assentos == ["Ana", "Bia", None, None]` e o trunfo ainda não preparado
- **THEN** a tela mostra `2 de 4`, os dois nomes e os dois assentos vagos, e nenhuma tecla de jogada manda `jogar`

### Test: os assentos mostram a contagem de cartas
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Espera pela mesa completa — CRITICAL
- **GIVEN** o snapshot com `assentos == ["Ana", "Bia", "Caio", "Duda"]` e `contagens == [10, 9, 10, 10]`
- **WHEN** a tela desenha o snapshot
- **THEN** ao lado de cada nome aparece a contagem daquele assento, e a contagem sai de `contagens`, não de um número fixo

### Test: os assentos contam os nomes com um assento vago no meio
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Espera pela mesa completa — EDGE
- **GIVEN** `assentos == ["Ana", None, "Caio", "Duda"]`, pelo helper puro `desenhar_assentos`
- **WHEN** o snapshot é desenhado
- **THEN** a contagem mostra `3 de 4` e o assento 1 aparece como vago

### Test: a mão desenha as cartas com o naipe colorido
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Mão de cartas em texto — CRITICAL
- **GIVEN** as cartas `"7H"` (copas), `"7C"` (paus), `"AD"` (ouros) e `"AS"` (espadas)
- **WHEN** cada uma é desenhada pelo helper de tela (função pura, sem `App`)
- **THEN** copas e ouros trazem `♥`/`♦` com marcação de vermelho, paus e espadas trazem `♣`/`♠` sem cor de naipe, e o valor sai em cima do símbolo

### Test: a mesa mostra trunfo, vaza e placar
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Mão de cartas em texto — CRITICAL
- **GIVEN** o snapshot com `carta_trunfo == "AH"`, `vaza == [(0, "7H"), (1, "AC")]` e `partidas == [1, 2]`
- **WHEN** a tela desenha o snapshot
- **THEN** o painel da mesa mostra a carta do trunfo (`A♥`, de `carta_trunfo`), as duas cartas jogadas junto do assento de quem jogou e o placar das duas duplas

### Test: a mesa desenha a vaza vazia e a vaza cheia
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Mão de cartas em texto — EDGE
- **GIVEN** um snapshot sem vaza e outro com quatro jogadas, pelo helper puro `desenhar_mesa`
- **WHEN** cada um é desenhado
- **THEN** o primeiro mostra só o trunfo e o placar, e o segundo mostra as quatro cartas com o assento de quem jogou

### Test: ←/→ movem a seleção e Enter joga a carta
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Jogada pela seleção — CRITICAL
- **GIVEN** o snapshot com a mão `["7H", "AC", "QS"]` e `vez == meu_assento`
- **WHEN** o teste aperta `→` e depois `Enter` (com `pilot.press` e `pilot.pause`)
- **THEN** o falso recebe `jogar` com a carta do meio (`AC`), e o destaque estava visível na tela antes do `Enter`

### Test: EDGE - a seleção não passa dos limites da mão
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Jogada pela seleção — EDGE
- **GIVEN** a mão `["7H", "AC", "QS"]`
- **WHEN** o teste aperta `←` na primeira carta e `→` quatro vezes
- **THEN** a seleção fica na última carta, sem índice negativo nem `IndexError`; `Enter` manda a última carta

### Test: EDGE - fora da vez o servidor decide
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Jogada pela seleção — EDGE
- **GIVEN** o snapshot com `vez` em outro assento
- **WHEN** o teste aperta `Enter`
- **THEN** o cliente manda `jogar` mesmo assim (o falso recebe a intenção) e a tela mostra o `erro` com o motivo que o falso devolver — o cliente não tem cópia da regra de vez

### Test: EDGE - a seleção volta à primeira carta com a mão nova
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Jogada pela seleção — EDGE
- **GIVEN** a seleção na terceira carta da mão
- **WHEN** o snapshot seguinte traz outra mão
- **THEN** o destaque volta à primeira carta, e o próximo `Enter` manda a primeira carta da mão nova

### Test: EDGE - com a mão vazia nada é jogado
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Jogada pela seleção — EDGE
- **GIVEN** o snapshot da espera, com `mao == []`
- **WHEN** o teste aperta `Enter`
- **THEN** o falso não recebe `jogar` nenhum (só o `entrar` inicial)
- **WHEN** o teste aperta `←` e `→`
- **THEN** a seleção continua em 0, sem `IndexError` nem `jogar` no fio

### Test: cima ou baixo abre na tela do respondente
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Pergunta cima ou baixo — CRITICAL
- **GIVEN** o cliente `"Ana"` no assento 1 e o snapshot com `assentos == ["Bia", "Ana", "Caio", "Duda"]`, `respondente == 1` e o trunfo não preparado
- **WHEN** a tela desenha o snapshot
- **THEN** o diálogo cima ou baixo está aberto (`app.screen` é a `RespostaScreen`) com as duas respostas

### Test: cima ou baixo responde
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Pergunta cima ou baixo — CRITICAL
- **GIVEN** o diálogo aberto
- **WHEN** o teste aperta `c`
- **THEN** o falso recebe `responder` com `cima` verdadeiro e o diálogo fecha
- **WHEN** um novo snapshot reabre o diálogo e o teste aperta `b`
- **THEN** o falso recebe `responder` com `cima` falso e o diálogo fecha

### Test: EDGE - quem não é o respondente não vê o diálogo
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Pergunta cima ou baixo — EDGE
- **GIVEN** o cliente `"Ana"` no assento 1 e o snapshot com `respondente == 2`
- **WHEN** a tela desenha o snapshot
- **THEN** o diálogo não abre e a tela segue na espera; e quando o snapshot seguinte traz o trunfo preparado, nenhum diálogo pendente fica na pilha

### Test: a queda aparece na tela
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Tela de queda — CRITICAL
- **GIVEN** a mesa em jogo com quatro nomes em `assentos`
- **WHEN** o snapshot traz `ausentes == [2]`
- **THEN** o aviso mostra o nome do assento 2 como caído e que a mesa está congelada, e a mão continua desenhada

### Test: EDGE - reconexão limpa a tela de queda
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Tela de queda — EDGE
- **GIVEN** a tela com o aviso de queda desenhado
- **WHEN** o snapshot seguinte traz `ausentes == []`
- **THEN** o aviso de queda some e a tela volta a mostrar a mesa em jogo

### Test: EDGE - congelado o cliente ainda manda e o servidor recusa
**Traces**: `sprints/06-cliente-tui/specs/cliente/spec.md` → Requirement: Tela de queda — EDGE
- **GIVEN** o snapshot com `ausentes == [2]` e a mão `["7H", "AC"]`
- **WHEN** o teste aperta `Enter`
- **THEN** o falso recebe `jogar` (nenhum guard local de congelamento) e a tela mostra `mesa_congelada` quando o falso devolve o `erro`

## Capability: comando

### Test: o cliente lê nome, host e porta
**Traces**: `sprints/06-cliente-tui/specs/comando/spec.md` → Requirement: Cliente na linha de comando — CRITICAL
- **GIVEN** o `argv` `["Ana", "--host", "10.0.0.2", "--porta", "9000"]`
- **WHEN** o parsing do comando é chamado (função pura, sem subir a tela)
- **THEN** o resultado é nome `Ana`, host `10.0.0.2` e porta `9000`

### Test: o cliente usa os defaults
**Traces**: `sprints/06-cliente-tui/specs/comando/spec.md` → Requirement: Cliente na linha de comando — CRITICAL
- **GIVEN** o `argv` `["Ana"]`
- **WHEN** o parsing roda
- **THEN** o host é `127.0.0.1` e a porta é `8765`

### Test: o servidor lê host e porta
**Traces**: `sprints/06-cliente-tui/specs/comando/spec.md` → Requirement: Servidor na linha de comando — CRITICAL
- **GIVEN** o `argv` `["--porta", "9000"]`
- **WHEN** o parsing do servidor roda
- **THEN** o host é `127.0.0.1` (default) e a porta é `9000`

### Test: o servidor usa a porta default
**Traces**: `sprints/06-cliente-tui/specs/comando/spec.md` → Requirement: Servidor na linha de comando — CRITICAL
- **GIVEN** o `argv` vazio
- **WHEN** o parsing do servidor roda
- **THEN** o host é `127.0.0.1` e a porta é `8765`

### Test: EDGE - argumento desconhecido sai com erro
**Traces**: `sprints/06-cliente-tui/specs/comando/spec.md` → Requirement: Cliente na linha de comando — EDGE
- **GIVEN** o `argv` `["Ana", "--turbo"]`
- **WHEN** o parsing roda
- **THEN** ele termina com `SystemExit` de código diferente de zero e nenhuma conexão é aberta

## Casos Limite

- A conexão cai antes de o snapshot chegar: o aviso de conexão aparece, sem tela de espera nem exceção no loop (o `finally` único do worker da decisão 10).
- Mão vazia: `Enter` não manda nada e a seleção fica em 0; o mesmo vale para a espera e para a mesa encerrada.
- A tela é idempotente: dois `Estado` iguais seguidos não mudam nada, e um `Estado` que chega com o diálogo aberto e o trunfo preparado fecha o diálogo.
- `assentos` com `None` no meio: a contagem `N de 4` conta só os nomes, e o assento de outro jogador aparece como vago.
- `vaza` com zero e com quatro jogadas: o painel desenha os dois casos sem quebrar.
- `encerrado` verdadeiro com `partidas == [4, 0]`: a 06 só desenha o placar; a tela final é da 07 (não objetivo).
- Linha acima do limite de leitura do cliente: tratada como fim de conexão (decisão 10); nenhum servidor legítimo a produz, e o teto do protocolo é defesa do servidor.
- Mesa congelada: as teclas de jogada seguem ativas (nenhum bloqueio local, decisão 4) e quem recusa é o servidor com `mesa_congelada`; o modal do cima/baixo não se confunde com o congelamento, porque a pergunta não depende de `ausentes`.
- O `erro` guardado no aviso sobrevive até o próximo snapshot (decisão 14): o teste do erro manda um `estado` depois para limpar.
- Dois clientes na mesma máquina sem nome distinto: o segundo recebe `erro nome_em_uso` na tela e para na tela de espera — comportamento documentado no roteiro.
- O roteiro do `README.md` usa os nomes como argumento posicional; nada no código deriva nome de usuário do sistema.

## Pontos de Integração

- `protocolo.serializar`/`desserializar` (`protocolo.py:95,162`) são o único codec entre o cliente e o servidor falso — o falso também os usa, então o teste cobre os dois sentidos com o código real.
- `Estado` (`protocolo.py:47`) é lido campo a campo pela tela: `assentos`, `mao`, `contagens`, `trunfo`, `carta_trunfo`, `vez`, `respondente`, `vaza`, `partidas`, `encerrado` e `ausentes`; nenhum widget vê o tipo.
- `Carta.de_texto` (`carta.py:72`) traduz o texto da mão em `Jogar`, e o texto da vaza é desenhado direto com o símbolo do naipe — um único formato de carta (`carta.py:71`).
- `Servidor.iniciar` (`servidor.py:35`) é o que o `main()` do servidor chama; o cliente nunca importa `servidor.py`.
- O roteiro do `README.md` (`README.md:56`) e os dois scripts do `pyproject.toml:12` precisam concordar: um erro de nome de comando só aparece na leitura humana.
- O assento derivado do nome depende da unicidade garantida pela 05 (`nome_em_uso`); se a 05 mudar, a tela perde a referência de "quem sou eu".

## Notas de Revisão

- **NÃO TESTÁVEL**: `specs/comando/spec.md` → Scenario: `o README traz o roteiro de quatro terminais` — é prosa; o grill decidiu leitura manual (task 10.5) e nenhum teste de documentação, porque a 07 reescreve essa seção. O cenário segue normativo na spec.
- **RED esperado verde (cobertura, não RED independente)**: `mensagem inválida do fio não derruba o app` exercita o mesmo ramo do `erro` (decisão 12); `com a mão vazia nada é jogado` e `a seleção não passa dos limites` são ramos do guard da seleção; `congelado o cliente ainda manda e o servidor recusa` exercita o envio sem guard de `Enter` com o aviso de `erro` já pronto (decisão 4 do grill). A lição das sprints 01–03 é não declarar RED para o que a implementação adjacente já cobre — estes entram como EDGE, com a implementação no mesmo ciclo do vizinho.
- **O que o grill fechou (Questões Abertas do `design.md`):** modal para o cima/baixo e painel para a queda, sem bloqueio local das teclas; nome posicional obrigatório; dois entrypoints; roteiro do `README.md` só com leitura manual; `erro` no `#aviso` até o próximo snapshot, sem `notify`; `toggle_dark` sai (a 07 re-liga); `contagens` no `#assentos` e `carta_trunfo` no `#mesa`.
- **Cobertura dos caminhos novos:** o gate `uv run pytest --cov=pysueca --cov-fail-under=80` (lição da 04) depende de `test_cliente.py` cobrir o `main.py` reescrito e o `main()` novo do `servidor.py`; o `App.run_test` cria widgets e workers, então o worker sem servidor precisa do seu próprio teste para não virar linha descoberta.
- **Asserção é sobre a tela, não sobre o tipo:** os testes leem o texto renderizado dos painéis (`Static.render().plain`), nunca `Estado`; se um widget importar `protocolo`, o teste não muda — a fronteira fica na revisão e no `AGENTS.md`.
- **Determinismo:** nenhum `sleep`; o falso notifica cada mensagem numa fila lida com `asyncio.wait_for`, e a tela é lida depois de `pilot.pause()` (decisão 9, lição da 05).
- **Retrabalho da verificação (2026-10-12):** o `b` do cima ou baixo, o fim de conexão (EOF e teto do leitor), a vaza vazia/cheia, o `None` no meio e a seleção com a mão vazia ganham teste; a implementação da 06 já cobria todos, então as tasks 11.x são cobertura declarada, não RED independente.

# QA Plan — Sprint 02 — Vaza e mão

> **Sprint:** `sprints/02-vaza-e-mao/` — rastreia `sprints/02-vaza-e-mao/specs/<capability>/spec.md`

## Capability: vaza

### Test: Assento com o naipe puxado é obrigado a jogá-lo
**Traces**: `sprints/02-vaza-e-mao/specs/vaza/spec.md` → Requirement: Seguir o naipe puxado — CRITICAL
- **GIVEN** uma `Mao(0, random.Random(1))` preparada, o assento da vez com carta de copas e de paus na mão e uma vaza de copas puxado
- **WHEN** o assento joga a carta de paus
- **THEN** `Mao.jogar` devolve `ErroJogada.NAO_SEGUIU_NAIPE` e a carta continua na mão

### Test: Assento sem o naipe puxado pode jogar qualquer carta (trunfar)
**Traces**: `sprints/02-vaza-e-mao/specs/vaza/spec.md` → Requirement: Seguir o naipe puxado — CRITICAL
- **GIVEN** uma `Mao` preparada, uma vaza de copas puxado com trunfo ouros e o assento da vez sem nenhuma carta de copas
- **WHEN** ele joga o Dois de ouros (trunfo)
- **THEN** `Mao.jogar` devolve `None` e a vaza passa a ter essa jogada

### Test: Ao puxar, qualquer carta da mão é aceita
**Traces**: `sprints/02-vaza-e-mao/specs/vaza/spec.md` → Requirement: Seguir o naipe puxado — CRITICAL
- **GIVEN** uma `Mao` preparada e a vez do embaralhador, com a vaza ainda vazia
- **WHEN** ele joga uma carta qualquer da própria mão
- **THEN** `Mao.jogar` devolve `None` e o naipe puxado da vaza é o naipe dessa carta

### Test: Trunfo vence o naipe puxado
**Traces**: `sprints/02-vaza-e-mao/specs/vaza/spec.md` → Requirement: Vencedor da vaza — CRITICAL
- **GIVEN** uma vaza `Vaza(Naipe.COPAS, Naipe.OUROS)` com o Ás de copas do assento 0 e o Dois de ouros do assento 1
- **WHEN** se lê `Vaza.vencedor`
- **THEN** é o assento 1

### Test: Entre trunfos vence a maior
**Traces**: `sprints/02-vaza-e-mao/specs/vaza/spec.md` → Requirement: Vencedor da vaza — CRITICAL
- **GIVEN** uma vaza com trunfo ouros e o Rei de ouros do assento 0 e o Sete de ouros do assento 1
- **WHEN** se lê `Vaza.vencedor`
- **THEN** é o assento 1 (Sete tem mais força que Rei)

### Test: Maior força do naipe puxado vence os descartes
**Traces**: `sprints/02-vaza-e-mao/specs/vaza/spec.md` → Requirement: Vencedor da vaza — CRITICAL
- **GIVEN** uma vaza `Vaza(Naipe.COPAS, Naipe.OUROS)` com Ás de copas (assento 0), Rei de copas (assento 1), Ás de paus (assento 2) e Dois de espadas (assento 3)
- **WHEN** se lê `Vaza.vencedor`
- **THEN** é o assento 0, e o Ás de paus descartado não vence

## Capability: mao

### Test: Preparação distribui 10 cartas por assento
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Preparação da mão — CRITICAL
- **GIVEN** uma `Mao(0, random.Random(42))`
- **WHEN** `preparar(cima=True)` roda
- **THEN** os quatro assentos têm 10 cartas cada e a união é exatamente o baralho de 40 cartas, sem repetição

### Test: A carta do trunfo fica com o dador
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Preparação da mão — CRITICAL
- **GIVEN** uma `Mao(embaralhador=0, random.Random(42))` (dador = assento 3)
- **WHEN** `preparar(cima=True)` roda
- **THEN** `carta_trunfo` está entre as cartas do assento 3 e `trunfo` é o naipe dela

### Test: Cima ou baixo escolhe a ponta do baralho
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Preparação da mão — CRITICAL
- **GIVEN** dois `Baralho(random.Random(42))` embaralhados, um de referência para o topo e outro para a base
- **WHEN** uma `Mao(0, random.Random(42))` prepara com `cima=True` e outra com `cima=False`
- **THEN** `carta_trunfo` é a primeira carta do baralho embaralhado num caso e a última no outro

### Test: Quem levou a vaza puxa a seguinte
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Sequência de vazas — CRITICAL
- **GIVEN** uma `Mao` preparada e uma vaza que fecha com o assento 1 como vencedor
- **WHEN** a vaza termina
- **THEN** `Mao.vez` é o assento 1, que passa a puxar a vaza seguinte

### Test: Mão completa são 10 vazas e esvazia as mãos
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Sequência de vazas — CRITICAL
- **GIVEN** uma `Mao(0, random.Random(7))` preparada e um RNG que sempre escolhe uma carta legal do assento da vez
- **WHEN** se jogam as 10 vazas
- **THEN** `Mao.vazas` tem 10 vazas e nenhuma carta sobra em nenhuma mão

### Test: Jogada fora da vez devolve erro
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Jogada ilegal devolve erro — EDGE
- **GIVEN** uma `Mao` preparada com a vez do assento 0
- **WHEN** o assento 2 tenta jogar uma carta da própria mão
- **THEN** `Mao.jogar` devolve `ErroJogada.FORA_DA_VEZ`

### Test: Carta fora da mão devolve erro
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Jogada ilegal devolve erro — EDGE
- **GIVEN** o assento da vez
- **WHEN** ele tenta jogar uma carta que pertence a outro assento
- **THEN** `Mao.jogar` devolve `ErroJogada.CARTA_FORA_DA_MAO`

### Test: Jogada ilegal não altera o estado
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Jogada ilegal devolve erro — EDGE
- **GIVEN** uma `Mao` com uma vaza em andamento
- **WHEN** uma jogada é recusada (fora da vez ou fora do naipe puxado)
- **THEN** `vez`, a vaza em andamento e as mãos ficam idênticos ao estado anterior

### Test: Pontuação da mão jogada
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Pontuação e resultado — CRITICAL
- **GIVEN** a mão jogada por completo do teste "Mão completa são 10 vazas"
- **WHEN** se leem `Mao.pontos` e `Mao.resultado`
- **THEN** cada dupla tem a soma dos pontos das vazas que venceu (assentos 0 e 2 / 1 e 3), o total é 120 e `resultado` é `Resultado.de_pontos(*pontos)`

### Test: EDGE - Resultado pelos limites do README
**Traces**: `sprints/02-vaza-e-mao/specs/mao/spec.md` → Requirement: Pontuação e resultado — EDGE
- **GIVEN** os placares 60–60, 61–59, 90–30, 91–29, 119–1 e 120–0
- **WHEN** `Resultado.de_pontos` classifica cada placar
- **THEN** são, respectivamente, `EMPATE`, `NORMAL`, `NORMAL`, `QUILO`, `QUILO` e `BANDEIRA`

## Casos Limite

- Jogada fora da vez é recusada mesmo sendo uma carta legal para a vaza (validação de assento antes da de naipe).
- Jogada ilegal não muta nada: `Mao.jogar` valida tudo antes de remover carta, avançar a vez ou criar vaza.
- Assento sem o naipe puxado é livre para jogar qualquer carta — inclusive uma carta de outro naipe que não seja trunfo (descarte).
- Fronteiras do resultado: 90 (normal) vs 91 (quilo), 119 (quilo) vs 120 (bandeira), 60–60 (empate).
- `cima=False` retira a última carta do baralho embaralhado, não a primeira.

## Pontos de Integração

- `Mao.preparar` consome `Baralho(rng)` e `embaralhar()` da sprint 01 — nenhuma mudança no `baralho.py`.
- `Vaza.vencedor` consome `Carta.vence(naipe_puxado, trunfo)` da sprint 01 — nenhuma regra de precedência reimplementada.
- `Resultado` e `ErroJogada` viram vocabulário do `protocolo.py` (sprint 04) para a mensagem de `erro`: o protocolo só formata o `ErroJogada`; a checagem de vez, posse e naipe fica no motor.
- `Jogo` (sprint 03) lê `Mao.pontos`/`Mao.resultado` e passa um `embaralhador` rotacionado.
- `pyproject.toml` não muda: nenhuma dependência nova (`docs/adr/0004`).

## Notas de Revisão

- **RESOLVIDO no grill**: `Mao.jogar` único cobre puxar e seguir; o protocolo (04) não terá mensagem própria de puxar.
- **RESOLVIDO no grill**: erros de regra no motor (`ErroJogada`); o `protocolo.py` (04) só formata o erro recebido — sem checagem de vez/posse duplicada.
- **RESOLVIDO no grill**: sem ADR nova para a distribuição reduzida; o modelo fica no `design.md` e o PLANO passa a citar `docs/adr/0003`.
- **Cobertura, não RED**: "Entre trunfos vence a maior" e "Maior força do naipe puxado vence os descartes" nascem verdes pelo reuso de `Carta.vence` (design, decisão 1) e ficam como prova da agregação.
- **Delegado à sprint 03**: `Resultado.partidas` (4/2/1/0) e a dupla vencedora da mão não entram nesta sprint.

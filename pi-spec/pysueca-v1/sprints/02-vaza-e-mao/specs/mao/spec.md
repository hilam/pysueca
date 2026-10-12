# Spec — Capability `mao`

> **Sprint:** `sprints/02-vaza-e-mao/` — capability `mao` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Preparação da mão
A mão SHALL preparar embaralhando as 40 cartas com o RNG injetado, retirando do baralho a carta do trunfo da ponta sorteada (cima = primeira carta, baixo = última), distribuindo 10 cartas para cada um dos quatro assentos e entregando a carta do trunfo ao dador — o assento três posições à frente do embaralhador. O naipe da carta do trunfo MUST ser o trunfo da mão. As 40 cartas MUST ficar particionadas entre os assentos, sem repetição.

#### Scenario: dez cartas por assento
- **WHEN** uma mão é preparada
- **THEN** os quatro assentos têm 10 cartas cada e juntos cobrem as 40 cartas do baralho, sem repetição

#### Scenario: a carta do trunfo fica com o dador
- **WHEN** uma mão com embaralhador no assento 0 é preparada
- **THEN** a carta do trunfo está na mão do assento 3 (o dador) e o trunfo é o naipe dela

#### Scenario: cima ou baixo escolhe a ponta do baralho
- **WHEN** duas mãos com o mesmo seed preparam, uma com `cima=True` e outra com `cima=False`
- **THEN** a carta do trunfo é, respectivamente, a primeira e a última carta do baralho embaralhado

### Requirement: Sequência de vazas
A mão SHALL abrir a primeira vaza pelo embaralhador, andar a vez na ordem 0→1→2→3→0 e, ao fechar a vaza de quatro cartas, dar a vez de puxar a seguinte ao assento vencedor. A mão SHALL ter exatamente 10 vazas, ao fim das quais todas as mãos ficam vazias.

#### Scenario: quem levou puxa a seguinte
- **WHEN** a vaza fecha com o assento 1 como vencedor
- **THEN** a vez passa a ser do assento 1, que abre a vaza seguinte

#### Scenario: dez vazas esvaziam as mãos
- **WHEN** as 10 vazas de uma mão são jogadas
- **THEN** existem 10 vazas concluídas e nenhuma carta sobra nas mãos

### Requirement: Jogada ilegal devolve erro
`Mao.jogar` SHALL devolver `ErroJogada` em vez de lançar exceção quando a jogada é ilegal, e MUST NOT alterar o estado da mão. Assento fora da vez, carta que não está na mão do assento e carta que não segue o naipe puxado SHALL ser recusados, cada um com o seu erro.

#### Scenario: jogada fora da vez
- **WHEN** um assento que não é o da vez tenta jogar
- **THEN** `Mao.jogar` devolve `ErroJogada.FORA_DA_VEZ`

#### Scenario: carta fora da mão
- **WHEN** o assento da vez tenta jogar uma carta que está com outro assento
- **THEN** `Mao.jogar` devolve `ErroJogada.CARTA_FORA_DA_MAO`

#### Scenario: jogada ilegal não altera o estado
- **WHEN** uma jogada recusada é tentada
- **THEN** a mão, a vez e a vaza em andamento ficam exatamente como estavam

### Requirement: Pontuação e resultado
Ao fim das 10 vazas, a mão SHALL somar os pontos das cartas conquistadas por dupla — assentos 0 e 2, assentos 1 e 3 —, totalizando 120, e SHALL classificar o resultado pelos limites do README: 120 pontos bandeira, 91 a 119 quilo, 61 a 90 vitória normal e 60 a 60 empate.

#### Scenario: pontos das duplas somam 120
- **WHEN** as 10 vazas de uma mão terminam
- **THEN** a soma dos pontos das duas duplas é 120 e cada dupla leva os pontos das vazas que venceu

#### Scenario: resultado pelos limites do README
- **WHEN** placares de 60 a 60, 61 a 59, 90 a 30, 91 a 29, 119 a 1 e 120 a 0 são classificados
- **THEN** são, respectivamente, empate, vitória normal, vitória normal, quilo, quilo e bandeira

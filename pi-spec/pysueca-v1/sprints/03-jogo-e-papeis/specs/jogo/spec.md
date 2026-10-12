# Spec — Capability `jogo`

> **Sprint:** `sprints/03-jogo-e-papeis/` — capability `jogo` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Rotação de papéis
O jogo SHALL ter um embaralhador por mão, começando pelo assento em que o jogo foi criado (A na primeira mão) e andando um assento a cada mão seguinte, na ordem 0→1→2→3→0. O embaralhador MUST puxar a primeira vaza da mão. Os demais papéis — dador, cortador e respondente — derivam do embaralhador e SHALL andar com ele.

#### Scenario: o embaralhador puxa a primeira vaza
- **WHEN** uma mão é preparada
- **THEN** `Mao.vez` é o assento do embaralhador, que abre a primeira vaza

#### Scenario: papéis andam um assento por mão
- **WHEN** uma mão se encerra e a seguinte é preparada
- **THEN** o embaralhador é o assento seguinte ao da mão anterior, e o dador é o assento três posições à frente dele

### Requirement: Placar de partidas
O jogo SHALL acumular partidas por dupla — assentos 0 e 2 contra assentos 1 e 3. Ao encerrar a mão, SHALL somar à dupla vencedora as partidas que o resultado vale (1 normal, 2 quilo, 4 bandeira) e MUST NOT somar partida alguma no empate de 60 a 60.

#### Scenario: mão normal soma uma partida
- **WHEN** uma mão termina com a dupla dos assentos 0 e 2 vencendo
- **THEN** o placar daquela dupla sobe uma partida e o da outra não muda

#### Scenario: quilo soma duas partidas ao vencedor
- **WHEN** uma mão termina em quilo
- **THEN** a dupla vencedora soma duas partidas

#### Scenario: empate de 60 a 60 não dá partida
- **WHEN** uma mão termina 60 a 60
- **THEN** nenhuma dupla soma partida

### Requirement: Fim do jogo
O jogo SHALL encerrar quando uma dupla alcançar 4 partidas; a bandeira vale 4 e cai nessa regra. O quilo vale 2 partidas e MUST NOT encerrar o jogo por si. Depois de encerrado, o jogo MUST NOT abrir nova mão, e SHALL declarar a dupla vencedora.

#### Scenario: bandeira encerra o jogo na hora
- **WHEN** uma mão termina em bandeira
- **THEN** a dupla vencedora alcança 4 partidas e o jogo fica encerrado

#### Scenario: quilo não encerra o jogo
- **WHEN** um quilo deixa a dupla vencedora com 2 partidas, abaixo de 4
- **THEN** o jogo continua e não fica encerrado

#### Scenario: jogo acaba ao chegar a 4 partidas
- **WHEN** uma dupla acumula a quarta partida em mãos normais
- **THEN** o jogo fica encerrado e a dupla vencedora é a que alcançou 4

#### Scenario: jogo encerrado não abre nova mão
- **WHEN** a mão é encerrada com o jogo já decidido
- **THEN** nenhum novo embaralhador entra e nenhuma nova mão é preparada

# Spec — Capability `vaza`

> **Sprint:** `sprints/02-vaza-e-mao/` — capability `vaza` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Seguir o naipe puxado
A vaza SHALL aceitar somente cartas da mão do assento da vez; havendo naipe puxado, o assento que tiver alguma carta daquele naipe MUST jogar uma delas, e a jogada de outro naipe MUST ser recusada sem alterar o estado. O assento sem carta do naipe puxado MAY jogar qualquer carta da mão, inclusive trunfo (trunfar). Ao puxar (primeira carta da vaza), qualquer carta da mão SHALL ser aceita e o naipe puxado passa a ser o da carta.

#### Scenario: assento com o naipe puxado é obrigado a jogá-lo
- **WHEN** o assento da vez, com copas e paus na mão, joga uma carta de paus numa vaza de copas puxado
- **THEN** a jogada é recusada com `ErroJogada.NAO_SEGUIU_NAIPE` e a carta continua na mão

#### Scenario: assento sem o naipe puxado pode jogar qualquer carta
- **WHEN** o assento da vez, sem nenhuma carta de copas, joga o Dois de trunfo numa vaza de copas puxado
- **THEN** a jogada é aceita e a carta entra na vaza

#### Scenario: ao puxar, qualquer carta da mão é aceita
- **WHEN** o embaralhador, dono da primeira vaza, joga uma carta qualquer da própria mão
- **THEN** a jogada é aceita e o naipe puxado é o naipe dessa carta

### Requirement: Vencedor da vaza
A vaza SHALL apontar como vencedor o assento que jogou a carta de maior precedência: trunfo sobre qualquer outro naipe; entre trunfos, a maior força; sem trunfo, a maior força do naipe puxado. Descartes de outros naipes MUST NOT vencer, por mais força que tenham.

#### Scenario: trunfo vence o naipe puxado
- **WHEN** uma vaza de copas puxado, trunfo ouros, tem o Ás de copas do assento 0 e o Dois de ouros do assento 1
- **THEN** o vencedor é o assento 1

#### Scenario: entre trunfos vence a maior
- **WHEN** uma vaza, com ouros de trunfo, tem o Rei de ouros do assento 0 e o Sete de ouros do assento 1
- **THEN** o vencedor é o assento 1

#### Scenario: maior força do naipe puxado vence os descartes
- **WHEN** uma vaza de copas puxado, trunfo ouros, tem o Ás de copas do assento 0, o Rei de copas do assento 1, o Ás de paus do assento 2 e o Dois de espadas do assento 3
- **THEN** o vencedor é o assento 0

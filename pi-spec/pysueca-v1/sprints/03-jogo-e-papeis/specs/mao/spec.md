# Spec — Capability `mao`

> **Sprint:** `sprints/03-jogo-e-papeis/` — capability `mao` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## MODIFIED Requirements

### Requirement: Pontuação e resultado
Ao fim das 10 vazas, a mão SHALL somar os pontos das cartas conquistadas por dupla — assentos 0 e 2, assentos 1 e 3 —, totalizando 120, e SHALL classificar o resultado pelos limites do README: 120 pontos bandeira, 91 a 119 quilo, 61 a 90 vitória normal e 60 a 60 empate. O resultado SHALL declarar quantas partidas vale para a dupla vencedora: 4 na bandeira, 2 no quilo, 1 na vitória normal e 0 no empate.

#### Scenario: pontos das duplas somam 120
- **WHEN** as 10 vazas de uma mão terminam
- **THEN** a soma dos pontos das duas duplas é 120 e cada dupla leva os pontos das vazas que venceu

#### Scenario: resultado pelos limites do README
- **WHEN** placares de 60 a 60, 61 a 59, 90 a 30, 91 a 29, 119 a 1 e 120 a 0 são classificados
- **THEN** são, respectivamente, empate, vitória normal, vitória normal, quilo, quilo e bandeira

#### Scenario: partidas que a mão vale
- **WHEN** os resultados empate, vitória normal, quilo e bandeira são lidos em partidas
- **THEN** valem, respectivamente, 0, 1, 2 e 4 partidas

# Spec — Capability `baralho`

> **Sprint:** `sprints/01-carta-e-baralho/` — capability `baralho` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Baralho de 40 cartas
O baralho SHALL conter exatamente uma carta para cada combinação dos 4 naipes com os 10 valores, totalizando 40 cartas distintas.

#### Scenario: 40 cartas distintas
- **WHEN** um baralho novo é criado
- **THEN** tem 40 cartas e nenhuma repetida

#### Scenario: cada naipe tem os 10 valores
- **WHEN** o baralho é agrupado por naipe
- **THEN** cada um dos 4 naipes tem os mesmos 10 valores

#### Scenario: pontos do baralho completo
- **WHEN** os pontos das 40 cartas de um baralho novo são somados
- **THEN** o total é 120

### Requirement: Embaralhamento preserva as cartas
O baralho SHALL oferecer embaralhamento que reordena as cartas sem perder nem duplicar nenhuma.

#### Scenario: embaralhar preserva as 40 cartas
- **WHEN** um baralho novo é embaralhado
- **THEN** continua com as mesmas 40 cartas distintas

### Requirement: RNG injetado
O baralho SHALL usar o `random.Random` recebido na construção; sem argumento MUST criar uma instância própria e MUST NOT usar o módulo `random` global. Com a mesma seed, o embaralhamento MUST ser determinístico.

#### Scenario: mesma seed, mesma ordem
- **WHEN** dois baralhos são embaralhados com instâncias de `random.Random` de seed igual
- **THEN** as duas ordens de carta são idênticas

#### Scenario: seeds diferentes embaralham diferente
- **WHEN** dois baralhos são embaralhados com seeds diferentes
- **THEN** as ordens são diferentes

#### Scenario: embaralha sem o random global
- **WHEN** as funções `random.shuffle` e `random.randrange` do módulo `random` são substituídas por versões que levantam erro
- **THEN** `embaralhar()` funciona usando apenas o RNG próprio do baralho

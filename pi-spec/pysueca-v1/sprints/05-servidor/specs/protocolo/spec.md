# Spec — Capability `protocolo` (modificada)

> **Sprint:** `sprints/05-servidor/` — capability `protocolo` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` e `sprints/04-protocolo/specs/protocolo/spec.md`

<!-- SHALL/MUST permanecem em inglês mesmo em texto português. -->

## ADDED Requirements

(nenhum)

## MODIFIED Requirements

### Requirement: Snapshot por assento
O snapshot `estado` SHALL ser montado por destinatário: SHALL trazer a mão inteira do assento destinatário e apenas a **contagem** de cartas de cada assento — as cartas alheias MUST NOT aparecer em campo algum. O snapshot SHALL trazer ainda os assentos ocupados, os **assentos ausentes** (`ausentes`: os assentos cujo dono caiu e continua reservado, sem conexão), o trunfo e a carta do trunfo, quem deve responder "cima ou baixo", a vaza em andamento, o placar de partidas e o fim do jogo.

#### Scenario: snapshot traz a própria mão
- **WHEN** um snapshot é montado para um assento
- **THEN** o campo da mão traz exatamente as cartas daquele assento

#### Scenario: snapshot traz só a contagem das outras mãos
- **WHEN** um snapshot é montado para um assento
- **THEN** as outras mãos aparecem somente como contagem de cartas, e nenhuma carta alheia aparece na linha

#### Scenario: snapshot reflete a mesa
- **WHEN** um snapshot é montado para uma mesa com trunfo virado, vaza em andamento e placar
- **THEN** traz o trunfo, a carta do trunfo, a vez, a vaza, o placar e o fim do jogo

#### Scenario: snapshot diz quem deve responder
- **WHEN** um snapshot é montado com a pergunta "cima ou baixo" pendente
- **THEN** `respondente` traz o assento que deve responder, e `None` quando não há pergunta

#### Scenario: snapshot diz quem caiu
- **WHEN** um snapshot é montado para uma mesa com um assento reservado sem conexão
- **THEN** `ausentes` traz esse assento, e uma mesa sem queda traz `ausentes` vazio

## REMOVED Requirements

(nenhum)

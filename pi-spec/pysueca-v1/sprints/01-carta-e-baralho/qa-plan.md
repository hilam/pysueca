# QA Plan — Sprint 01 — Carta e baralho

> **Sprint:** `sprints/01-carta-e-baralho/` — rastreia `sprints/01-carta-e-baralho/specs/<capability>/spec.md`

## Capability: carta

### Test: Carta formada por naipe e valor
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Carta é par de naipe e valor — CRITICAL
- **GIVEN** os enums `Naipe` e `Valor`
- **WHEN** se cria `Carta(Naipe.COPAS, Valor.SETE)`
- **THEN** `.naipe` é copas e `.valor` é Sete

### Test: Pontos dos valores com ponto
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Pontos por valor — CRITICAL
- **GIVEN** os valores Ás, Sete, Rei, Valete e Dama
- **WHEN** se lê os pontos de cada um
- **THEN** são 11, 10, 4, 3 e 2, nessa ordem

### Test: EDGE - Valor sem ponto vale zero
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Pontos por valor (edge case) — EDGE
- **GIVEN** os valores Seis, Cinco, Quatro, Três e Dois
- **WHEN** se lê os pontos de cada um
- **THEN** todos valem 0

### Test: Soma dos pontos do baralho é 120
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Pontos por valor — CRITICAL
- **GIVEN** um baralho novo com as 40 cartas
- **WHEN** os pontos das 40 cartas são somados
- **THEN** o total é 120

### Test: Ás mais forte que Sete
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Força independente dos pontos — CRITICAL
- **GIVEN** as cartas Ás e Sete
- **WHEN** se compara a força das duas
- **THEN** o Ás é mais forte e tem mais força que o Sete

### Test: EDGE - Força entre cartas de 0 ponto
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Força independente dos pontos (edge case) — EDGE
- **GIVEN** as cartas Seis e Dois (ambas 0 ponto)
- **WHEN** se compara a força das duas
- **THEN** o Seis é mais forte

### Test: "7H" ida e volta preserva naipe e valor
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Texto ida-e-volta — CRITICAL
- **GIVEN** o texto `"7H"`
- **WHEN** `Carta.de_texto("7H")` é convertido e depois `carta.texto()`
- **THEN** o resultado é `"7H"`, com naipe copas e valor Sete

### Test: EDGE - Texto inválido rejeitado
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Texto ida-e-volta (edge case) — EDGE
- **GIVEN** o texto `"7X"` (naipe inexistente)
- **WHEN** se chama `Carta.de_texto("7X")`
- **THEN** levanta `ValueError`

### Test: Ás de trunfo vence qualquer carta
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza — CRITICAL
- **GIVEN** o Ás de copas com copas como trunfo, um naipe puxado e as outras 39 cartas
- **WHEN** o Ás de trunfo é comparado com cada uma delas via `vence(outra, naipe_puxado, trunfo)`
- **THEN** `vence` devolve verdadeiro para todas

### Test: Entre trunfos vence a maior
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza — CRITICAL
- **GIVEN** o Sete de trunfo e o Rei de trunfo (naipe puxado = trunfo)
- **WHEN** o Sete de trunfo é comparado com o Rei de trunfo via `vence(outra, naipe_puxado, trunfo)`
- **THEN** o Sete de trunfo vence

### Test: Naipe puxado vence o descarte de força maior
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza — CRITICAL
- **GIVEN** o Rei de copas, o Ás de paus, naipe puxado copas e trunfo ouros
- **WHEN** o Rei de copas é comparado com o Ás de paus
- **THEN** o Rei de copas vence, apesar da força maior do Ás de paus

### Test: Trunfo vence o naipe puxado
**Traces**: `sprints/01-carta-e-baralho/specs/carta/spec.md` → Requirement: Desempate de duas cartas na vaza — CRITICAL
- **GIVEN** o Dois de trunfo e o Ás de copas, sendo copas o naipe puxado
- **WHEN** o Dois de trunfo é comparado com o Ás de copas via `vence(outra, naipe_puxado, trunfo)`
- **THEN** o Dois de trunfo vence

## Capability: baralho

### Test: Baralho tem 40 cartas distintas
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: Baralho de 40 cartas — CRITICAL
- **GIVEN** um `Baralho()` novo
- **WHEN** se lê as cartas
- **THEN** são 40 e todas distintas

### Test: Cada naipe tem os 10 valores
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: Baralho de 40 cartas — CRITICAL
- **GIVEN** um `Baralho()` novo
- **WHEN** as cartas são agrupadas por naipe
- **THEN** cada um dos 4 naipes tem os 10 valores

### Test: Pontos do baralho completo somam 120
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: Baralho de 40 cartas — CRITICAL
- **GIVEN** um `Baralho()` novo
- **WHEN** os pontos das 40 cartas são somados
- **THEN** o total é 120

### Test: Mesma seed, mesma ordem
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: RNG injetado — CRITICAL
- **GIVEN** dois `Baralho(random.Random(42))`
- **WHEN** os dois são embaralhados
- **THEN** a ordem das cartas é idêntica

### Test: EDGE - Seeds diferentes embaralham diferente
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: RNG injetado (edge case) — EDGE
- **GIVEN** um `Baralho(random.Random(1))` e um `Baralho(random.Random(2))`
- **WHEN** os dois são embaralhados
- **THEN** as ordens são diferentes

### Test: Embaralhar preserva as 40 cartas
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: Embaralhamento preserva as cartas — CRITICAL
- **GIVEN** um `Baralho(random.Random(7))` e a lista de cartas antes
- **WHEN** o baralho é embaralhado
- **THEN** continua com 40 cartas distintas, o mesmo conjunto de antes

### Test: EDGE - Embaralha sem o random global
**Traces**: `sprints/01-carta-e-baralho/specs/baralho/spec.md` → Requirement: RNG injetado (edge case) — EDGE
- **GIVEN** `random.shuffle` e `random.randrange` do módulo substituídos por versões que levantam erro
- **WHEN** `Baralho().embaralhar()` é chamado
- **THEN** o embaralhamento funciona, usando apenas o RNG próprio do baralho

## Casos Limite

- `Carta.de_texto` com naipe inválido (`"7X"`) e valor inválido (`"1H"`) → `ValueError`.
- Valores de 0 ponto (Seis a Dois) mantêm força decrescente.
- `Baralho()` sem RNG não usa o módulo `random` global — com `random.shuffle`/`random.randrange` monkeypatchados para explodir, `embaralhar()` funciona.
- Descarte de força maior perde para o naipe puxado.

## Pontos de Integração

- `Carta.vence(outra, naipe_puxado, trunfo)` será consumido pelo `motor.py` na sprint 02 para decidir quem leva a vaza.
- `Carta.de_texto`/`texto()` serão reusados pelo `protocolo.py` na sprint 04 — o formato de fio fecha aqui.
- `pyproject.toml` não muda: nenhuma dependência nova (`docs/adr/0004`).

## Notas de Revisão

- Nenhuma pendência — a divergência de "Valor" no glossário foi resolvida no `design.md` (Decisão 2).

# Spec — Capability `carta`

> **Sprint:** `sprints/01-carta-e-baralho/` — capability `carta` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Carta é par de naipe e valor
O motor SHALL representar uma carta como a combinação de um `Naipe` (paus, copas, espadas, ouros) e um `Valor` (Ás, Sete, Rei, Valete, Dama, Seis, Cinco, Quatro, Três, Dois), conforme `CONTEXT.md`.

#### Scenario: carta formada por naipe e valor
- **WHEN** se cria uma carta com naipe copas e valor Sete
- **THEN** a carta expõe naipe copas e valor Sete

### Requirement: Pontos por valor
O motor SHALL atribuir pontos somente pelos valores que os têm: Ás 11, Sete 10, Rei 4, Valete 3, Dama 2; Seis, Cinco, Quatro, Três e Dois MUST valer 0. A soma das 40 cartas de um baralho MUST ser 120.

#### Scenario: pontos dos valores com ponto
- **WHEN** as cartas Ás, Sete, Rei, Valete e Dama são pontuadas
- **THEN** valem, respectivamente, 11, 10, 4, 3 e 2

#### Scenario: valor sem ponto
- **WHEN** uma carta de valor Dois é pontuada
- **THEN** vale 0 pontos

### Requirement: Força independente dos pontos
O motor SHALL ordenar a força dos valores como Ás > Sete > Rei > Valete > Dama > Seis > Cinco > Quatro > Três > Dois. Essa ordem MUST NOT ser derivada dos pontos — Seis a Dois empatam em 0 ponto e ainda assim têm força distinta.

#### Scenario: força do Ás e do Sete
- **WHEN** se comparam a força do Ás e do Sete
- **THEN** o Ás é mais forte, apesar de o Sete valer quase os mesmos pontos

#### Scenario: força entre cartas de 0 ponto
- **WHEN** se comparam a força do Seis e do Dois
- **THEN** o Seis é mais forte, apesar de ambos valerem 0 ponto

### Requirement: Texto ida-e-volta
O motor SHALL converter carta de e para texto no formato `<valor><naipe>`, com valor em `A,7,K,J,Q,6,5,4,3,2` e naipe em `C` (paus), `H` (copas), `S` (espadas), `D` (ouros). A conversão de ida e volta MUST preservar naipe e valor, e texto fora do formato MUST ser rejeitado com erro.

#### Scenario: "7H" ida e volta
- **WHEN** `"7H"` é convertido em carta e a carta é convertida de volta em texto
- **THEN** o resultado é `"7H"`, com naipe copas e valor Sete

#### Scenario: texto inválido rejeitado
- **WHEN** se converte o texto `"7X"` (naipe inexistente)
- **THEN** a conversão falha com `ValueError`

#### Scenario: texto de tamanho errado rejeitado
- **WHEN** se converte um texto com tamanho diferente de 2 (`"7HH"`, `"7"` ou `""`)
- **THEN** a conversão falha com `ValueError`

### Requirement: Desempate de duas cartas na vaza
O motor SHALL decidir qual de duas cartas vence, dada a vaza por `(outra, naipe_puxado, trunfo)`: uma carta de trunfo vence qualquer carta que não seja de trunfo; sem trunfo na disputa, uma carta do naipe puxado vence qualquer carta de outro naipe (descarte); e, entre cartas do mesmo naipe, MUST vencer a de maior força.

#### Scenario: Ás de trunfo vence qualquer carta
- **WHEN** o Ás de trunfo é comparado com cada uma das outras 39 cartas, sob qualquer naipe puxado
- **THEN** o Ás de trunfo vence todas

#### Scenario: entre trunfos vence a maior
- **WHEN** o Sete de trunfo é comparado com o Rei de trunfo, sendo o naipe puxado o próprio trunfo
- **THEN** o Sete de trunfo vence

#### Scenario: trunfo vence o naipe puxado
- **WHEN** o Dois de trunfo é comparado com o Ás de copas, sendo copas o naipe puxado
- **THEN** o Dois de trunfo vence

#### Scenario: naipe puxado vence o descarte de força maior
- **WHEN** o Rei de copas é comparado com o Ás de paus, sendo copas o naipe puxado e ouros o trunfo
- **THEN** o Rei de copas vence, apesar de o Ás de paus ser a carta mais forte

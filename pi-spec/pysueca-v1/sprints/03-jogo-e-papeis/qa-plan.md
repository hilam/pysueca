# QA Plan — Sprint 03 — Jogo e papéis

> **Sprint:** `sprints/03-jogo-e-papeis/` — rastreia `sprints/03-jogo-e-papeis/specs/<capability>/spec.md`

## Capability: mao

### Test: Partidas que a mão vale
**Traces**: `sprints/03-jogo-e-papeis/specs/mao/spec.md` → Requirement: Pontuação e resultado — CRITICAL
- **GIVEN** os quatro resultados da mão
- **WHEN** se lê `Resultado.partidas` de empate, vitória normal, quilo e bandeira
- **THEN** valem 0, 1, 2 e 4 partidas, respectivamente

## Capability: jogo

### Test: O embaralhador puxa a primeira vaza
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Rotação de papéis — CRITICAL
- **GIVEN** um `Jogo(random.Random(7), embaralhador=0)` que ainda não preparou a mão
- **WHEN** `Jogo.preparar(cima=True)` roda
- **THEN** `Jogo.mao.vez` é o assento 0 (o embaralhador) e a primeira jogada aceita por `Jogo.jogar` é dele

### Test: Papéis andam um assento por mão
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Rotação de papéis — CRITICAL
- **GIVEN** um `Jogo(random.Random(7), embaralhador=0)` com a primeira mão inteira jogada
- **WHEN** `Jogo.encerrar_mao()` fecha a mão e a seguinte é preparada
- **THEN** o embaralhador é o assento 1, `Jogo.mao.embaralhador` também, o dador é o assento 0 (`(1+3)%4`) e a vez de puxar é do assento 1

### Test: Jogo.jogar devolve o erro do motor
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Rotação de papéis — EDGE
- **GIVEN** um `Jogo` com a mão preparada e a vez do assento 0
- **WHEN** o assento 2 tenta jogar por `Jogo.jogar`
- **THEN** devolve `ErroJogada.FORA_DA_VEZ` sem alterar o estado (a validação continua só no motor)

### Test: Mão normal soma uma partida à dupla vencedora
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Placar de partidas — CRITICAL
- **GIVEN** um `Jogo` com a mão corrente valendo 70 a 50 para a dupla dos assentos 0 e 2
- **WHEN** `Jogo.encerrar_mao()` soma a mão
- **THEN** `Jogo.partidas` é `[1, 0]`

### Test: Quilo soma duas partidas à dupla vencedora
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Placar de partidas — CRITICAL
- **GIVEN** um `Jogo` com a mão corrente valendo 29 a 91 para a dupla dos assentos 1 e 3
- **WHEN** `Jogo.encerrar_mao()` soma a mão
- **THEN** `Jogo.partidas` é `[0, 2]`

### Test: EDGE - Empate de 60 a 60 não dá partida
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Placar de partidas — EDGE
- **GIVEN** um `Jogo` com a mão corrente valendo 60 a 60
- **WHEN** `Jogo.encerrar_mao()` soma a mão
- **THEN** `Jogo.partidas` continua `[0, 0]`, o jogo não encerra e o embaralhador já andou um assento

### Test: EDGE - Bandeira encerra o jogo na hora
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo — CRITICAL
- **GIVEN** um `Jogo` com a mão corrente valendo 120 a 0 para a dupla dos assentos 0 e 2
- **WHEN** `Jogo.encerrar_mao()` soma a mão
- **THEN** `Jogo.partidas` é `[4, 0]`, `Jogo.encerrado` é verdadeiro e `Jogo.vencedor` é 0

### Test: Quilo não encerra o jogo
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo — CRITICAL
- **GIVEN** um `Jogo` com a mão corrente valendo 100 a 20 para a dupla dos assentos 0 e 2
- **WHEN** `Jogo.encerrar_mao()` soma a mão
- **THEN** `Jogo.partidas` é `[2, 0]` e `Jogo.encerrado` continua falso — a corrida vai até 4 partidas

### Test: Jogo acaba ao chegar a 4 partidas
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo — CRITICAL
- **GIVEN** um `Jogo` em que a dupla dos assentos 0 e 2 vence quatro mãos normais seguidas
- **WHEN** a quarta mão é somada
- **THEN** `Jogo.partidas` é `[4, 0]`, `Jogo.encerrado` é verdadeiro e `Jogo.vencedor` é 0

### Test: EDGE - Jogo encerrado não abre nova mão
**Traces**: `sprints/03-jogo-e-papeis/specs/jogo/spec.md` → Requirement: Fim do jogo — EDGE
- **GIVEN** um `Jogo` já encerrado por bandeira, com o embaralhador e a mão anotados
- **WHEN** `Jogo.encerrar_mao()` é chamado de novo
- **THEN** `Jogo.embaralhador` e `Jogo.mao` não mudam (nenhuma nova mão é aberta)

## Casos Limite

- Fronteira do placar: quilo para a dupla 1 (`[0, 2]`) prova que o vencedor não está chumbado na dupla 0.
- Empate 60–60 tem `Resultado.partidas == 0` e não computa dupla vencedora (decisão 5 do `design.md`).
- Bandeira para a dupla 0 e quatro mãos normais para a dupla 0 chegam ao mesmo `encerrado` por caminhos diferentes — a regra é `max(partidas) >= 4`, uma só (decisão 8).
- Quilo com a dupla vencedora abaixo de 4 partidas (ex.: `[2, 0]`) não encerra — a corrida só termina em 4.
- `encerrar_mao` depois do jogo encerrado não rotaciona nem recria a `Mao` (o servidor checa `encerrado` antes de `preparar`).
- `Jogo.jogar` não duplica validação: erro de vez/posse/naipe continua vindo da `Mao`.

## Pontos de Integração

- `Jogo` cria `Mao(embaralhador, rng)` e repassa o RNG do construtor — o mesmo RNG injetado das sprints 01/02, sem `random` global (`docs/adr/0004`).
- `Jogo.encerrar_mao` lê `Mao.pontos` e `Mao.resultado` e usa `Resultado.partidas` — nenhuma reclassificação de limites no `Jogo`.
- `Jogo.jogar` devolve `ErroJogada` da `Mao`; o `protocolo.py` (04) vai formatar o mesmo enum, sem reinterpretar regra.
- `Jogo.partidas`/`encerrado`/`vencedor` alimentam o snapshot do protocolo (04) e a tela final (06).
- `pyproject.toml` não muda: nenhuma dependência nova (`docs/adr/0004`).

## Notas de Revisão

- **RESOLVIDO no grill**: quilo **não** encerra o jogo (decisão 8); só 4 partidas encerram e `README.md`/`CONTEXT.md` recebem errata.
- **RESOLVIDO no grill**: `Jogo.vencedor` entra nesta sprint — a dupla vencedora é regra de jogo, lida pela TUI (06) e pelo snapshot (04) (decisão 9).
- **RESOLVIDO no grill**: `encerrar_mao()` devolve `Resultado`, para o servidor (05) anunciar o desfecho sem depender da ordem de leitura (decisão 3).
- **Cobertura, não RED**: `Quilo soma duas partidas`, `Quilo não encerra o jogo`, `Bandeira encerra na hora` e `Jogo acaba ao chegar a 4` compartilham a linha `self.partidas[dupla] += resultado.partidas` e a condição `max(partidas) >= 4`; o primeiro deles fica RED e os demais provam o mesmo caminho com entradas diferentes (lição das sprints 01/02: não inflar a implementação para forçar vermelho).
- **Teste com placar forçado**: os cenários de placar trocam `jogo.mao` por uma subclasse de `Mao` com `pontos` fixo, definida só no `tests/test_jogo.py` — o motor não ganha fábrica nem parâmetro de injeção de mão.

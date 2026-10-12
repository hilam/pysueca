# Tasks — Sprint 02 — Vaza e mão

> **Sprint:** `sprints/02-vaza-e-mao/` — rastreia `sprints/02-vaza-e-mao/qa-plan.md`, `sprints/02-vaza-e-mao/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [ ] 1.1 Criar branch `feat/pysueca-v1-02-vaza-e-mao` — scope `<id>` nos commits
- [ ] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 02-vaza-e-mao — vaza e mão` (`sprints/02-vaza-e-mao/*.md` + `specs/**`)

## 2. Vaza — vencedor (RED → GREEN)

- [ ] 2.1 Teste do cenário `Trunfo vence o naipe puxado` (RED)
- [ ] 2.2 `src/pysueca/motor.py`: `Naipe` importado, `Vaza(naipe_puxado, trunfo, jogadas)` e `vencedor` reduzindo por `Carta.vence` (GREEN)
- [ ] 2.3 Commit: `test(02-vaza-e-mao): trunfo vence o naipe puxado` → `feat(02-vaza-e-mao): adiciona Vaza com vencedor`

- [ ] 2.4 Testes dos cenários `Entre trunfos vence a maior` e `Maior força do naipe puxado vence os descartes` (RED esperado verde — cobertura do reuso de `Carta.vence`; ver `design.md` Decisão 1)
- [ ] 2.5 Nenhuma implementação nova (GREEN)
- [ ] 2.6 Commit: `test(02-vaza-e-mao): cobre desempate entre trunfos e descartes`

## 3. Mão — preparação (RED → GREEN)

- [ ] 3.1 Teste do cenário `Preparação distribui 10 cartas por assento` (RED)
- [ ] 3.2 `Mao(embaralhador, rng=None)` com `preparar(cima=True)`: `Baralho(rng)`, `embaralhar()` e rodízio de 10 cartas por assento (GREEN)
- [ ] 3.3 Commit: `test(02-vaza-e-mao): preparação distribui 10 cartas por assento` → `feat(02-vaza-e-mao): adiciona Mao e a distribuição`

- [ ] 3.4 Teste do cenário `A carta do trunfo fica com o dador` (RED)
- [ ] 3.5 `preparar` retira a ponta do baralho, entrega a carta ao dador `(embaralhador + 3) % 4` e expõe `trunfo` e `carta_trunfo` (GREEN)
- [ ] 3.6 Commit: `test(02-vaza-e-mao): carta do trunfo fica com o dador` → `feat(02-vaza-e-mao): define o trunfo e o dador`

- [ ] 3.7 Teste do cenário `Cima ou baixo escolhe a ponta do baralho` (RED)
- [ ] 3.8 `preparar(cima)` retirando `cartas[0]` ou `cartas[-1]` (GREEN)
- [ ] 3.9 Commit: `test(02-vaza-e-mao): cima ou baixo escolhe a ponta` → `feat(02-vaza-e-mao): aceita cima ou baixo na preparação`

## 4. Mão — jogadas e vez (RED → GREEN)

- [ ] 4.1 Teste do cenário `Ao puxar, qualquer carta da mão é aceita` (RED)
- [ ] 4.2 `Mao.jogar(assento, carta)` mínimo: vez, carta na mão, abre a `Vaza` e anda a vez (GREEN)
- [ ] 4.3 Commit: `test(02-vaza-e-mao): ao puxar qualquer carta é aceita` → `feat(02-vaza-e-mao): adiciona jogar e a abertura da vaza`

- [ ] 4.4 Teste do cenário `Assento com o naipe puxado é obrigado a jogá-lo` (RED)
- [ ] 4.5 `jogada_legal(mao, naipe_puxado, carta)` recusando carta de outro naipe com `ErroJogada.NAO_SEGUIU_NAIPE` (GREEN)
- [ ] 4.6 Commit: `test(02-vaza-e-mao): naipe puxado é obrigatório` → `feat(02-vaza-e-mao): exige seguir o naipe puxado`

- [ ] 4.7 Teste do cenário `Assento sem o naipe puxado pode jogar qualquer carta (trunfar)` (RED)
- [ ] 4.8 `jogada_legal` libera a carta quando a mão não tem o naipe puxado (GREEN)
- [ ] 4.9 Commit: `test(02-vaza-e-mao): sem o naipe puxado, qualquer carta` → `feat(02-vaza-e-mao): permite trunfar quando falta o naipe`

- [ ] 4.10 Teste do cenário `Quem levou a vaza puxa a seguinte` (RED)
- [ ] 4.11 Ao fechar 4 jogadas, mover a `Vaza` para `vazas` e dar a vez ao vencedor (GREEN)
- [ ] 4.12 Commit: `test(02-vaza-e-mao): quem levou puxa a seguinte` → `feat(02-vaza-e-mao): fecha a vaza e passa a vez`

- [ ] 4.13 Teste do cenário `Mão completa são 10 vazas e esvazia as mãos` (RED)
- [ ] 4.14 Confirmar o laço de 10 vazas com escolha de carta legal (GREEN)
- [ ] 4.15 Commit: `test(02-vaza-e-mao): mão completa são 10 vazas` → `test(02-vaza-e-mao): cobre a mão inteira`

## 5. Pontuação e resultado (RED → GREEN)

- [ ] 5.1 Teste do cenário `Pontuação da mão jogada` (RED)
- [ ] 5.2 `Mao.pontos` (dupla = `assento % 2`), `Mao.resultado` e `Resultado.de_pontos` com empate e vitória normal (GREEN)
- [ ] 5.3 Commit: `test(02-vaza-e-mao): pontuação da mão jogada` → `feat(02-vaza-e-mao): adiciona pontos e resultado da mão`

- [ ] 5.4 Teste do caso limite `EDGE - Resultado pelos limites do README` (RED)
- [ ] 5.5 `Resultado.de_pontos` acrescenta quilo (91 a 119) e bandeira (120) (GREEN)
- [ ] 5.6 Commit: `test(02-vaza-e-mao): limites do resultado` → `feat(02-vaza-e-mao): classifica quilo e bandeira`

## 6. Casos Limite e Robustez

- [ ] 6.1 Teste do caso limite `Jogada fora da vez devolve erro` (RED)
- [ ] 6.2 Guarda de vez em `Mao.jogar` devolvendo `ErroJogada.FORA_DA_VEZ` (GREEN)
- [ ] 6.3 Commit: `test(02-vaza-e-mao): cobre jogada fora da vez` → `feat(02-vaza-e-mao): recusa jogada fora da vez`

- [ ] 6.4 Teste do caso limite `Carta fora da mão devolve erro` (RED)
- [ ] 6.5 Guarda de posse da carta devolvendo `ErroJogada.CARTA_FORA_DA_MAO` (GREEN)
- [ ] 6.6 Commit: `test(02-vaza-e-mao): cobre carta fora da mão` → `feat(02-vaza-e-mao): recusa carta que não está na mão`

- [ ] 6.7 Teste do caso limite `Jogada ilegal não altera o estado` (RED esperado verde — cobertura das guardas de 6.2/6.5; registrar como cobertura)
- [ ] 6.8 Confirmar GREEN
- [ ] 6.9 Commit: `test(02-vaza-e-mao): jogada ilegal não altera o estado`

## 7. Refatoração (apenas no GREEN)

- [ ] 7.1 Refatorar `motor.py` mantendo todos os testes verdes (ex.: `Mao.jogar` delegando a validação numa única função, sem duplicar checagens)
- [ ] 7.2 Rodar a suite completa
- [ ] 7.3 Commit: `refactor(02-vaza-e-mao): centraliza a validação da jogada mantendo cobertura`

## 8. Validação Final

- [ ] 8.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [ ] 8.2 Tipos: `uv run mypy src`
- [ ] 8.3 Suite completa uma última vez: `uv run pytest`
- [ ] 8.4 Commit de ajustes finais: `style: aplica lint e formatação`

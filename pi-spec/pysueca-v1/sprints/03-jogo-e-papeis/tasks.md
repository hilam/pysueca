# Tasks — Sprint 03 — Jogo e papéis

> **Sprint:** `sprints/03-jogo-e-papeis/` — rastreia `sprints/03-jogo-e-papeis/qa-plan.md`, `sprints/03-jogo-e-papeis/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [ ] 1.1 Criar branch `feat/pysueca-v1-03-jogo-e-papeis` — scope `<id>` nos commits
- [ ] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 03-jogo-e-papeis — jogo e papéis` (`sprints/03-jogo-e-papeis/*.md` + `specs/**`)

## 2. Jogo — esqueleto (tracer bullet, RED → GREEN)

- [ ] 2.1 Teste do cenário `O embaralhador puxa a primeira vaza` (RED)
- [ ] 2.2 `src/pysueca/motor.py`: `Jogo(rng=None, embaralhador=0)` com `mao = Mao(embaralhador, rng)`, `preparar(cima=True)` e `jogar(assento, carta)` delegando à `Mao` (GREEN)
- [ ] 2.3 Commit: `test(03-jogo-e-papeis): embaralhador puxa a primeira vaza` → `feat(03-jogo-e-papeis): adiciona Jogo com preparar e jogar`

- [ ] 2.4 Teste do caso limite `Jogo.jogar devolve o erro do motor` (RED esperado verde — cobertura da delegação; ver `design.md` Decisão 2)
- [ ] 2.5 Nenhuma implementação nova (GREEN)
- [ ] 2.6 Commit: `test(03-jogo-e-papeis): Jogo.jogar devolve o erro do motor`

## 3. Resultado — partidas por mão (RED → GREEN)

- [ ] 3.1 Teste do cenário `Partidas que a mão vale` (RED)
- [ ] 3.2 `Resultado.partidas`: `EMPATE` 0, `NORMAL` 1, `QUILO` 2, `BANDEIRA` 4 (GREEN)
- [ ] 3.3 Commit: `test(03-jogo-e-papeis): partidas que a mão vale` → `feat(03-jogo-e-papeis): Resultado declara as partidas da mão`

## 4. Placar (RED → GREEN)

- [ ] 4.1 Teste do cenário `Mão normal soma uma partida à dupla vencedora` (RED)
- [ ] 4.2 `Jogo.encerrar_mao()` mínimo: empate devolve cedo; senão soma `resultado.partidas` à dupla vencedora (`pontos[0] > pontos[1]` → dupla 0, senão dupla 1) (GREEN)
- [ ] 4.3 Commit: `test(03-jogo-e-papeis): mão normal soma uma partida` → `feat(03-jogo-e-papeis): adiciona encerrar_mao e o placar`

- [ ] 4.4 Teste do cenário `Quilo soma duas partidas à dupla vencedora` (RED esperado verde — cobre o ramo da dupla 1 sobre o mesmo mapa de `partidas`; registrar como cobertura)
- [ ] 4.5 Nenhuma implementação nova (GREEN)
- [ ] 4.6 Commit: `test(03-jogo-e-papeis): quilo soma duas partidas à dupla 1`

- [ ] 4.7 Teste do caso limite `Empate de 60 a 60 não dá partida` (RED esperado verde — cobertura do curto-circuito do empate; ver `design.md` Decisão 5)
- [ ] 4.8 Nenhuma implementação nova (GREEN)
- [ ] 4.9 Commit: `test(03-jogo-e-papeis): empate não dá partida a ninguém`

## 5. Rotação de papéis (RED → GREEN)

- [ ] 5.1 Teste do cenário `Papéis andam um assento por mão` (RED)
- [ ] 5.2 `encerrar_mao` rotaciona `embaralhador = (embaralhador + 1) % 4`, cria a nova `Mao` com esse assento (mantendo a vez de puxar no embaralhador) e devolve o `Resultado` da mão encerrada (GREEN)
- [ ] 5.3 Commit: `test(03-jogo-e-papeis): papéis andam um assento por mão` → `feat(03-jogo-e-papeis): rotaciona o embaralhador e abre a mão seguinte`

## 6. Fim do jogo (RED → GREEN)

- [ ] 6.1 Teste do cenário `Bandeira encerra o jogo na hora` (RED)
- [ ] 6.2 `Jogo.encerrado` (`max(partidas) >= 4`), `Jogo.vencedor` (dupla que alcançou 4, `None` enquanto corre) e a mão seguinte só quando não encerrado (GREEN)
- [ ] 6.3 Commit: `test(03-jogo-e-papeis): bandeira encerra o jogo na hora` → `feat(03-jogo-e-papeis): encerra o jogo em 4 partidas`

- [ ] 6.4 Teste do cenário `Quilo não encerra o jogo` (RED esperado verde — mesma condição `>= 4` com a dupla vencedora em 2 partidas; registrar como cobertura)
- [ ] 6.5 Nenhuma implementação nova (GREEN)
- [ ] 6.6 Commit: `test(03-jogo-e-papeis): quilo não encerra o jogo`

- [ ] 6.7 Teste do cenário `Jogo acaba ao chegar a 4 partidas` (RED esperado verde — mesma condição `>= 4`, acúmulo em quatro mãos normais; registrar como cobertura)
- [ ] 6.8 Nenhuma implementação nova (GREEN)
- [ ] 6.9 Commit: `test(03-jogo-e-papeis): jogo acaba ao chegar a 4 partidas`

- [ ] 6.10 Teste do caso limite `Jogo encerrado não abre nova mão` (RED — o segundo `encerrar_mao` somaria o placar de novo)
- [ ] 6.11 Guarda de idempotência no topo de `encerrar_mao`: com o jogo encerrado, devolver o resultado sem somar nem rotacionar (GREEN)
- [ ] 6.12 Commit: `test(03-jogo-e-papeis): jogo encerrado não abre nova mão` → `feat(03-jogo-e-papeis): torna encerrar_mao idempotente`

## 7. Refatoração (apenas no GREEN)

- [ ] 7.1 Refatorar `motor.py` mantendo todos os testes verdes (ex.: extrair a dupla vencedora de `encerrar_mao` num único ponto, sem duplicar a comparação de pontos)
- [ ] 7.2 Rodar a suite completa
- [ ] 7.3 Commit: `refactor(03-jogo-e-papeis): extrai a dupla vencedora mantendo cobertura`

## 8. Validação Final

- [ ] 8.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [ ] 8.2 Tipos: `uv run mypy src`
- [ ] 8.3 Suite completa uma última vez: `uv run pytest`
- [ ] 8.4 Commit de ajustes finais: `style: aplica lint e formatação`

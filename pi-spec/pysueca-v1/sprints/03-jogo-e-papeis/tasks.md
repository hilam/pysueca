# Tasks — Sprint 03 — Jogo e papéis

> **Sprint:** `sprints/03-jogo-e-papeis/` — rastreia `sprints/03-jogo-e-papeis/qa-plan.md`, `sprints/03-jogo-e-papeis/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [x] 1.1 Criar branch `feat/pysueca-v1-03-jogo-e-papeis` — scope `<id>` nos commits
- [x] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 03-jogo-e-papeis — jogo e papéis` (`sprints/03-jogo-e-papeis/*.md` + `specs/**`)

## 2. Jogo — esqueleto (tracer bullet, RED → GREEN)

- [x] 2.1 Teste do cenário `O embaralhador puxa a primeira vaza` (RED)
- [x] 2.2 `src/pysueca/motor.py`: `Jogo(rng=None, embaralhador=0)` com `mao = Mao(embaralhador, rng)`, `preparar(cima=True)` e `jogar(assento, carta)` delegando à `Mao` (GREEN)
- [x] 2.3 Commit: `test(03-jogo-e-papeis): embaralhador puxa a primeira vaza` → `feat(03-jogo-e-papeis): adiciona Jogo com preparar e jogar`

- [x] 2.4 Teste do caso limite `Jogo.jogar devolve o erro do motor` (RED esperado verde — cobertura da delegação; ver `design.md` Decisão 2)
- [x] 2.5 Nenhuma implementação nova (GREEN)
- [x] 2.6 Commit: `test(03-jogo-e-papeis): Jogo.jogar devolve o erro do motor`

## 3. Resultado — partidas por mão (RED → GREEN)

- [x] 3.1 Teste do cenário `Partidas que a mão vale` (RED)
- [x] 3.2 `Resultado.partidas`: `EMPATE` 0, `NORMAL` 1, `QUILO` 2, `BANDEIRA` 4 (GREEN)
- [x] 3.3 Commit: `test(03-jogo-e-papeis): partidas que a mão vale` → `feat(03-jogo-e-papeis): Resultado declara as partidas da mão`

## 4. Placar (RED → GREEN)

- [x] 4.1 Teste do cenário `Mão normal soma uma partida à dupla vencedora` (RED)
- [x] 4.2 `Jogo.encerrar_mao()` mínimo: empate devolve cedo; senão soma `resultado.partidas` à dupla vencedora (`pontos[0] > pontos[1]` → dupla 0, senão dupla 1) (GREEN)
- [x] 4.3 Commit: `test(03-jogo-e-papeis): mão normal soma uma partida` → `feat(03-jogo-e-papeis): adiciona encerrar_mao e o placar`

- [x] 4.4 Teste do cenário `Quilo soma duas partidas à dupla vencedora` (RED esperado verde — cobre o ramo da dupla 1 sobre o mesmo mapa de `partidas`; registrar como cobertura)
- [x] 4.5 Nenhuma implementação nova (GREEN)
- [x] 4.6 Commit: `test(03-jogo-e-papeis): quilo soma duas partidas à dupla 1`

- [x] 4.7 Teste do caso limite `Empate de 60 a 60 não dá partida` (RED esperado verde — cobertura do curto-circuito do empate; ver `design.md` Decisão 5)
- [x] 4.8 Nenhuma implementação nova (GREEN)
- [x] 4.9 Commit: `test(03-jogo-e-papeis): empate não dá partida a ninguém`

## 5. Rotação de papéis (RED → GREEN)

- [x] 5.1 Teste do cenário `Papéis andam um assento por mão` (RED)
- [x] 5.2 `encerrar_mao` rotaciona `embaralhador = (embaralhador + 1) % 4`, cria a nova `Mao` com esse assento (mantendo a vez de puxar no embaralhador) e devolve o `Resultado` da mão encerrada (GREEN)
- [x] 5.3 Commit: `test(03-jogo-e-papeis): papéis andam um assento por mão` → `feat(03-jogo-e-papeis): rotaciona o embaralhador e abre a mão seguinte`

## 6. Fim do jogo (RED → GREEN)

- [x] 6.1 Teste do cenário `Bandeira encerra o jogo na hora` (RED)
- [x] 6.2 `Jogo.encerrado` (`max(partidas) >= 4`), `Jogo.vencedor` (dupla que alcançou 4, `None` enquanto corre) e a mão seguinte só quando não encerrado (GREEN)
- [x] 6.3 Commit: `test(03-jogo-e-papeis): bandeira encerra o jogo na hora` → `feat(03-jogo-e-papeis): encerra o jogo em 4 partidas`

- [x] 6.4 Teste do cenário `Quilo não encerra o jogo` (RED esperado verde — mesma condição `>= 4` com a dupla vencedora em 2 partidas; registrar como cobertura)
- [x] 6.5 Nenhuma implementação nova (GREEN)
- [x] 6.6 Commit: `test(03-jogo-e-papeis): quilo não encerra o jogo`

- [x] 6.7 Teste do cenário `Jogo acaba ao chegar a 4 partidas` (RED esperado verde — mesma condição `>= 4`, acúmulo em quatro mãos normais; registrar como cobertura)
- [x] 6.8 Nenhuma implementação nova (GREEN)
- [x] 6.9 Commit: `test(03-jogo-e-papeis): jogo acaba ao chegar a 4 partidas`

- [x] 6.10 Teste do caso limite `Jogo encerrado não abre nova mão` (RED — o segundo `encerrar_mao` somaria o placar de novo)
- [x] 6.11 Guarda de idempotência no topo de `encerrar_mao`: com o jogo encerrado, devolver o resultado sem somar nem rotacionar (GREEN)
- [x] 6.12 Commit: `test(03-jogo-e-papeis): jogo encerrado não abre nova mão` → `feat(03-jogo-e-papeis): torna encerrar_mao idempotente`

## 7. Refatoração (apenas no GREEN)

- [x] 7.1 Refatorar `motor.py` mantendo todos os testes verdes (ex.: extrair a dupla vencedora de `encerrar_mao` num único ponto, sem duplicar a comparação de pontos)
- [x] 7.2 Rodar a suite completa
- [x] 7.3 Commit: `refactor(03-jogo-e-papeis): extrai a dupla vencedora mantendo cobertura`

## 8. Validação Final

- [x] 8.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [x] 8.2 Tipos: `uv run mypy src`
- [x] 8.3 Suite completa uma última vez: `uv run pytest`
- [x] 8.4 Commit de ajustes finais: `style: aplica lint e formatação`

## Notas de Execução

- **8.1/8.2 (pré-existentes, não regressões):** `uv run ruff check` acusa 4 erros e `uv run ruff format --check` 2 arquivos — todos em `src/pysueca/main.py` e `src/pysueca/imagens/get_images.py`, endereçados na sprint 06 (`main.py` é reescrita). `motor.py` e `test_jogo.py` passam limpos em `ruff check`, `ruff format --check`.
- **8.4:** nenhum ajuste de lint/format nos arquivos tocados — sem commit `style:` (a suíte fechou verde com `pytest`).
- **Correção de artefato:** o `qa-plan.md` trazia o cenário de quilo como `41 a 79` (que é vitória normal, não quilo); corrigido para `29 a 91` no commit `docs(03-jogo-e-papeis): corrige o placar do cenário de quilo no qa-plan`.
- **Ordem do empate:** as asserções de rotação e `encerrado` do cenário 60–60 entraram junto dos REDs de rotação (task 5.1) e fim do jogo (task 6.1), mantendo cada asserção vermelha antes do seu GREEN.

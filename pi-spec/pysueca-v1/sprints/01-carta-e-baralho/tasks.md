# Tasks — Sprint 01 — Carta e baralho

> **Sprint:** `sprints/01-carta-e-baralho/` — rastreia `sprints/01-carta-e-baralho/qa-plan.md`, `sprints/01-carta-e-baralho/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [ ] 1.1 Criar branch `feat/pysueca-v1-01-carta-e-baralho` — scope `<id>` nos commits
- [ ] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 01-carta-e-baralho — carta e baralho` (`sprints/01-carta-e-baralho/*.md` + `specs/**`)

## 2. Testes (RED → GREEN)

Tracer bullet: a carta e o baralho ponta a ponta, na ordem de dependência (`carta.py` antes de `baralho.py`).

- [ ] 2.1 Teste do cenário `Carta formada por naipe e valor` (RED)
- [ ] 2.2 Implementação mínima de `Naipe`, `Valor` e `Carta` em `src/pysueca/carta.py` (GREEN)
- [ ] 2.3 Commit: `test(01-carta-e-baralho): carta é par de naipe e valor` → `feat(01-carta-e-baralho): adiciona Naipe, Valor e Carta`

- [ ] 2.4 Teste do cenário `Baralho tem 40 cartas distintas` (RED)
- [ ] 2.5 Implementação mínima de `Baralho` em `src/pysueca/baralho.py` (GREEN)
- [ ] 2.6 Commit: `test(01-carta-e-baralho): baralho tem 40 cartas distintas` → `feat(01-carta-e-baralho): adiciona Baralho de 40 cartas`

- [ ] 2.7 Teste do cenário `Cada naipe tem os 10 valores` (RED)
- [ ] 2.8 Ajuste da geração para garantir os 4 naipes × 10 valores (GREEN)
- [ ] 2.9 Commit: `test(01-carta-e-baralho): cada naipe tem os 10 valores` → `feat(01-carta-e-baralho): completa os naipes do baralho`

- [ ] 2.10 Teste do cenário `Pontos dos valores com ponto` (RED)
- [ ] 2.11 Implementação de `Valor.pontos` (GREEN)
- [ ] 2.12 Commit: `test(01-carta-e-baralho): pontos por valor` → `feat(01-carta-e-baralho): adiciona pontos de carta`

- [ ] 2.13 Teste do cenário `Soma dos pontos do baralho é 120` (RED)
- [ ] 2.14 Confirmação de que a soma fecha em 120 (GREEN)
- [ ] 2.15 Commit: `test(01-carta-e-baralho): soma do baralho é 120` → `test(01-carta-e-baralho): cobre soma de pontos`

- [ ] 2.16 Teste do cenário `Ás mais forte que Sete` (RED)
- [ ] 2.17 Implementação de `Valor.forca` na ordem `A > 7 > K > J > Q > 6 > 5 > 4 > 3 > 2` (GREEN)
- [ ] 2.18 Commit: `test(01-carta-e-baralho): força independente dos pontos` → `feat(01-carta-e-baralho): adiciona força de carta`

- [ ] 2.19 Teste do cenário `"7H" ida e volta` (RED)
- [ ] 2.20 Implementação de `Carta.de_texto`/`Carta.texto()` no formato de fio (GREEN)
- [ ] 2.21 Commit: `test(01-carta-e-baralho): texto ida e volta` → `feat(01-carta-e-baralho): adiciona de_texto e texto`

- [ ] 2.22 Teste do cenário `Ás de trunfo vence qualquer carta` (RED)
- [ ] 2.23 Implementação de `Carta.vence(outra, naipe_puxado, trunfo)` (GREEN)
- [ ] 2.24 Commit: `test(01-carta-e-baralho): Ás de trunfo vence qualquer carta` → `feat(01-carta-e-baralho): adiciona desempate de vaza`

- [ ] 2.25 Teste do cenário `Entre trunfos vence a maior` (RED)
- [ ] 2.26 Ajuste do desempate entre trunfos por força (GREEN)
- [ ] 2.27 Commit: `test(01-carta-e-baralho): entre trunfos vence a maior` → `feat(01-carta-e-baralho): desempata trunfos por força`

- [ ] 2.28 Teste do cenário `Naipe puxado vence o descarte de força maior` (RED)
- [ ] 2.29 Ajuste do desempate naipe puxado vs. descarte (GREEN)
- [ ] 2.30 Commit: `test(01-carta-e-baralho): naipe puxado vence o descarte` → `feat(01-carta-e-baralho): prioriza o naipe puxado no desempate`

- [ ] 2.31 Teste do cenário `Trunfo vence o naipe puxado` (RED)
- [ ] 2.32 Ajuste do desempate trunfo vs. naipe puxado (GREEN)
- [ ] 2.33 Commit: `test(01-carta-e-baralho): trunfo vence o naipe puxado` → `feat(01-carta-e-baralho): prioriza trunfo no desempate`

- [ ] 2.34 Teste do cenário `Mesma seed, mesma ordem` (RED)
- [ ] 2.35 Implementação do RNG injetado e de `embaralhar()` (GREEN)
- [ ] 2.36 Commit: `test(01-carta-e-baralho): RNG determinístico` → `feat(01-carta-e-baralho): injeta random.Random no Baralho`

- [ ] 2.37 Teste do cenário `Embaralhar preserva as 40 cartas` (RED)
- [ ] 2.38 Confirmação de que o embaralhamento não perde nem duplica (GREEN)
- [ ] 2.39 Commit: `test(01-carta-e-baralho): embaralhar preserva as cartas` → `test(01-carta-e-baralho): cobre preservação do baralho`

## 3. Casos Limite e Robustez

- [ ] 3.1 Teste do caso limite `EDGE - Valor sem ponto vale zero` (RED)
- [ ] 3.2 Implementação de pontos 0 para Seis a Dois (GREEN)
- [ ] 3.3 Commit: `test(01-carta-e-baralho): cobre valor sem ponto` → `feat(01-carta-e-baralho): pontua cartas de 0 ponto`

- [ ] 3.4 Teste do caso limite `EDGE - Força entre cartas de 0 ponto` (RED)
- [ ] 3.5 Ajuste da força dos valores de 0 ponto (GREEN)
- [ ] 3.6 Commit: `test(01-carta-e-baralho): cobre força de cartas de 0 ponto` → `feat(01-carta-e-baralho): desempata cartas de 0 ponto`

- [ ] 3.7 Teste do caso limite `EDGE - Texto inválido rejeitado` (RED)
- [ ] 3.8 Implementação de `ValueError` para valor/naipe inválido (GREEN)
- [ ] 3.9 Commit: `test(01-carta-e-baralho): cobre texto inválido` → `feat(01-carta-e-baralho): rejeita texto de carta inválido`

- [ ] 3.10 Teste do caso limite `EDGE - Seeds diferentes embaralham diferente` (RED)
- [ ] 3.11 Confirmação de que o RNG injetado diferencia as ordens (GREEN)
- [ ] 3.12 Commit: `test(01-carta-e-baralho): cobre seeds diferentes` → `test(01-carta-e-baralho): cobre variação por seed`

- [ ] 3.13 Teste do caso limite `EDGE - Embaralha sem o random global` (RED)
- [ ] 3.14 Implementação que só usa `self.rng`, nunca as funções do módulo `random` (GREEN)
- [ ] 3.15 Commit: `test(01-carta-e-baralho): cobre ausência do random global` → `feat(01-carta-e-baralho): usa só o RNG próprio do Baralho`

## 4. Documentação

Task sem `### Test:` — documentação não é capability; a verificação é a leitura do arquivo (referência: `PLANO-PYSUECA-V1.md` → Sprint 01 — Entregável).

- [ ] 4.1 Criar `AGENTS.md` na raiz com `uv run`, mapa de arquivos, as invariantes "motor puro e síncrono" e "só Textual", e o ponteiro para `docs/adr/` e `CONTEXT.md`. Incluir boas práticas de Python. Incluir Conventional Commits.
- [ ] 4.2 Commit: `docs(01-carta-e-baralho): adiciona AGENTS.md`

## 5. Refatoração (apenas no GREEN)

- [ ] 5.1 Refatorar `carta.py`/`baralho.py` mantendo todos os testes verdes (ex.: tabela de valores única, sem duplicar `pontos`/`forca`)
- [ ] 5.2 Rodar a suite completa
- [ ] 5.3 Commit: `refactor(01-carta-e-baralho): consolida tabela de valores mantendo cobertura`

## 6. Validação Final

- [ ] 6.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [ ] 6.2 Tipos: `uv run mypy src`
- [ ] 6.3 Suite completa uma última vez: `uv run pytest`
- [ ] 6.4 Commit de ajustes finais: `style: aplica lint e formatação`

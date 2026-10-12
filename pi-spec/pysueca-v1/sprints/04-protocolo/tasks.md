# Tasks — Sprint 04 — Protocolo

> **Sprint:** `sprints/04-protocolo/` — rastreia `sprints/04-protocolo/qa-plan.md`, `sprints/04-protocolo/specs/protocolo/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [ ] 1.1 Criar branch `feat/pysueca-v1-04-protocolo` — scope `04-protocolo` nos commits
- [ ] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 04-protocolo — protocolo` (`sprints/04-protocolo/*.md` + `specs/**`)

## 2. Mensagens do cliente (tracer bullet, RED → GREEN)

- [ ] 2.1 Teste do cenário `entrar faz ida-e-volta` (RED)
- [ ] 2.2 `src/pysueca/protocolo.py`: dataclasses `Entrar`/`Erro`, `serializar` (uma linha JSON em bytes UTF-8 com `\n`) e `desserializar` mínimo só para o tipo `entrar` (GREEN)
- [ ] 2.3 Commit: `test(04-protocolo): entrar faz ida-e-volta` → `feat(04-protocolo): adiciona o codec e a mensagem entrar`

- [ ] 2.4 Teste do cenário `jogar faz ida-e-volta` (RED)
- [ ] 2.5 `Jogar` com o campo `carta` via `Carta.texto()`/`Carta.de_texto()` (GREEN)
- [ ] 2.6 Commit: `test(04-protocolo): jogar faz ida-e-volta` → `feat(04-protocolo): adiciona a mensagem jogar com a carta "7H"`

- [ ] 2.7 Teste do cenário `responder faz ida-e-volta` (RED esperado verde — mesmo caminho de codec do 2.4; registrar como cobertura)
- [ ] 2.8 `Responder(cima: bool)` no codec (GREEN)
- [ ] 2.9 Commit: `test(04-protocolo): responder faz ida-e-volta` → `feat(04-protocolo): adiciona a mensagem responder`

## 3. Validação estrita recuperável (RED → GREEN)

- [ ] 3.1 Teste do caso limite `EDGE - linha malformada vira erro` (RED)
- [ ] 3.2 Guarda de JSON: `json.loads` em `try`, não-objeto e parse falho → `Erro(motivo="json_invalido")` sem levantar (GREEN)
- [ ] 3.3 Commit: `test(04-protocolo): linha malformada vira erro` → `feat(04-protocolo): recusa json inválido com erro recuperável`

- [ ] 3.4 Teste do caso limite `EDGE - tipo desconhecido vira erro` (RED)
- [ ] 3.5 Despacho por `tipo` com fallback → `Erro(motivo="tipo_desconhecido")` (GREEN)
- [ ] 3.6 Commit: `test(04-protocolo): tipo desconhecido vira erro` → `feat(04-protocolo): recusa tipo desconhecido`

- [ ] 3.7 Teste do caso limite `EDGE - campo faltando vira erro` (RED)
- [ ] 3.8 Validação de presença e tipo de cada campo obrigatório (`carta`, `nome`, `cima`) → `Erro(motivo="campo_faltando")` (GREEN)
- [ ] 3.9 Commit: `test(04-protocolo): campo faltando vira erro` → `feat(04-protocolo): valida os campos obrigatórios de cada mensagem`

- [ ] 3.10 Teste do cenário `nome é normalizado` (RED)
- [ ] 3.11 `Entrar` normaliza o nome com `strip` antes de virar identidade (GREEN)
- [ ] 3.12 Commit: `test(04-protocolo): nome é normalizado` → `feat(04-protocolo): normaliza o nome no codec`

- [ ] 3.13 Teste do caso limite `EDGE - nome inválido vira erro` (RED)
- [ ] 3.14 Guarda de 1 a 20 caracteres após o `strip` → `Erro(motivo="nome_invalido")` (GREEN)
- [ ] 3.15 Commit: `test(04-protocolo): nome inválido vira erro` → `feat(04-protocolo): limita o nome a 20 caracteres`

- [ ] 3.16 Teste do caso limite `EDGE - campo extra vira erro` (RED)
- [ ] 3.17 Validação do conjunto exato de chaves de cada mensagem → `Erro(motivo="campo_extra")` (GREEN)
- [ ] 3.18 Commit: `test(04-protocolo): campo extra vira erro` → `feat(04-protocolo): recusa campo desconhecido`

## 4. Teto de bytes por linha (RED → GREEN)

- [ ] 4.1 Teste do caso limite `EDGE - linha acima do teto é fatal` (RED)
- [ ] 4.2 `TETO_LINHA` (4096 bytes UTF-8, contando o `\n`, aplicado só na desserialização/leitura) e `LinhaLonga`, o único `raise` (GREEN)
- [ ] 4.3 Commit: `test(04-protocolo): linha acima do teto é fatal` → `feat(04-protocolo): sinaliza a linha acima do teto`

- [ ] 4.4 Teste do caso limite `EDGE - linha no limite é aceita` (RED esperado verde — cobre a fronteira `> TETO_LINHA` vs. `>=`; registrar como cobertura)
- [ ] 4.5 Nenhuma implementação nova (GREEN)
- [ ] 4.6 Commit: `test(04-protocolo): linha no limite é aceita`

- [ ] 4.7 Teste do caso limite `EDGE - nenhum outro erro é fatal` (RED esperado verde — ancora a distinção `Erro` vs. `LinhaLonga`; registrar como cobertura)
- [ ] 4.8 Nenhuma implementação nova (GREEN)
- [ ] 4.9 Commit: `test(04-protocolo): nenhum outro erro é fatal`

## 5. Snapshot por assento (RED → GREEN)

- [ ] 5.1 Teste do cenário `snapshot traz a própria mão` (RED)
- [ ] 5.2 `Estado` (dataclass com todos os campos) e `estado(jogo, nomes, assento)` preenchendo `assentos` e `mao` com as cartas do assento (GREEN)
- [ ] 5.3 Commit: `test(04-protocolo): snapshot traz a própria mão` → `feat(04-protocolo): adiciona o snapshot estado por assento`

- [ ] 5.4 Teste do cenário `estado faz ida-e-volta` (RED)
- [ ] 5.5 Codec do tipo `estado` no `serializar`/`desserializar` (GREEN)
- [ ] 5.6 Commit: `test(04-protocolo): estado faz ida-e-volta` → `feat(04-protocolo): serializa o snapshot`

- [ ] 5.7 Teste do caso limite `EDGE - snapshot traz só a contagem das outras mãos` (RED)
- [ ] 5.8 `contagens` com o tamanho de cada mão; as mãos alheias não entram em campo algum (GREEN)
- [ ] 5.9 Commit: `test(04-protocolo): snapshot traz só a contagem das outras mãos` → `feat(04-protocolo): mascara as mãos alheias no snapshot`

- [ ] 5.10 Teste do caso limite `EDGE - snapshot reflete a mesa` (RED)
- [ ] 5.11 `estado()` preenche `trunfo`, `carta_trunfo`, `vez`, `vaza`, `partidas`, `encerrado` e `vencedor` a partir do `Jogo` (GREEN)
- [ ] 5.12 Commit: `test(04-protocolo): snapshot reflete a mesa` → `feat(04-protocolo): completa o snapshot com o estado do jogo`

- [ ] 5.13 Teste do cenário `snapshot diz quem deve responder` (RED)
- [ ] 5.14 `estado()` preenche `respondente` — `(embaralhador + 1) % 4` com a mão não preparada, `None` com a mão preparada (GREEN)
- [ ] 5.15 Commit: `test(04-protocolo): snapshot diz quem deve responder` → `feat(04-protocolo): expõe quem responde cima ou baixo`

## 6. Erro de jogada formatado (RED → GREEN)

- [ ] 6.1 Teste do caso limite `EDGE - jogada fora da vez vira erro` (RED)
- [ ] 6.2 `erro_de_jogada(ErroJogada) -> Erro` com o mapa de motivos estáveis (GREEN)
- [ ] 6.3 Commit: `test(04-protocolo): jogada fora da vez vira erro` → `feat(04-protocolo): formata o ErroJogada como erro`

- [ ] 6.4 Teste do caso limite `EDGE - carta fora da mão vira erro` (RED esperado verde — mesmo mapa de 6.2; registrar como cobertura)
- [ ] 6.5 Nenhuma implementação nova (GREEN)
- [ ] 6.6 Commit: `test(04-protocolo): carta fora da mão vira erro`

- [ ] 6.7 Teste do caso limite `EDGE - não seguir o naipe vira erro` (RED esperado verde — mesmo mapa de 6.2; registrar como cobertura)
- [ ] 6.8 Nenhuma implementação nova (GREEN)
- [ ] 6.9 Commit: `test(04-protocolo): não seguir o naipe vira erro`

## 7. Refatoração (apenas no GREEN)

- [ ] 7.1 Refatorar `protocolo.py` mantendo todos os testes verdes (ex.: extrair a validação de shape de campo numa única função e o mapa `tipo → dataclass` num único ponto)
- [ ] 7.2 Rodar a suite completa
- [ ] 7.3 Commit: `refactor(04-protocolo): extrai a validação de campo e o despacho de tipo`

## 8. Validação Final

- [ ] 8.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [ ] 8.2 Tipos: `uv run mypy src`
- [ ] 8.3 Suite completa uma última vez: `uv run pytest`
- [ ] 8.4 Commit de ajustes finais: `style: aplica lint e formatação`

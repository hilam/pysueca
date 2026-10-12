# Tasks — Sprint 04 — Protocolo

> **Sprint:** `sprints/04-protocolo/` — rastreia `sprints/04-protocolo/qa-plan.md`, `sprints/04-protocolo/specs/protocolo/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [x] 1.1 Criar branch `feat/pysueca-v1-04-protocolo` — scope `04-protocolo` nos commits
- [x] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 04-protocolo — protocolo` (`sprints/04-protocolo/*.md` + `specs/**`)

## 2. Mensagens do cliente (tracer bullet, RED → GREEN)

- [x] 2.1 Teste do cenário `entrar faz ida-e-volta` (RED)
- [x] 2.2 `src/pysueca/protocolo.py`: dataclasses `Entrar`/`Erro`, `serializar` (uma linha JSON em bytes UTF-8 com `\n`) e `desserializar` mínimo só para o tipo `entrar` (GREEN)
- [x] 2.3 Commit: `test(04-protocolo): entrar faz ida-e-volta` → `feat(04-protocolo): adiciona o codec e a mensagem entrar`

- [x] 2.4 Teste do cenário `jogar faz ida-e-volta` (RED)
- [x] 2.5 `Jogar` com o campo `carta` via `Carta.texto()`/`Carta.de_texto()` (GREEN)
- [x] 2.6 Commit: `test(04-protocolo): jogar faz ida-e-volta` → `feat(04-protocolo): adiciona a mensagem jogar com a carta "7H"`

- [x] 2.7 Teste do cenário `responder faz ida-e-volta` (RED esperado verde — mesmo caminho de codec do 2.4; registrar como cobertura)
- [x] 2.8 `Responder(cima: bool)` no codec (GREEN)
- [x] 2.9 Commit: `test(04-protocolo): responder faz ida-e-volta` → `feat(04-protocolo): adiciona a mensagem responder`

## 3. Validação estrita recuperável (RED → GREEN)

- [x] 3.1 Teste do caso limite `EDGE - linha malformada vira erro` (RED)
- [x] 3.2 Guarda de JSON: `json.loads` em `try`, não-objeto e parse falho → `Erro(motivo="json_invalido")` sem levantar (GREEN)
- [x] 3.3 Commit: `test(04-protocolo): linha malformada vira erro` → `feat(04-protocolo): recusa json inválido com erro recuperável`

- [x] 3.4 Teste do caso limite `EDGE - tipo desconhecido vira erro` (RED)
- [x] 3.5 Despacho por `tipo` com fallback → `Erro(motivo="tipo_desconhecido")` (GREEN)
- [x] 3.6 Commit: `test(04-protocolo): tipo desconhecido vira erro` → `feat(04-protocolo): recusa tipo desconhecido`

- [x] 3.7 Teste do caso limite `EDGE - campo faltando vira erro` (RED)
- [x] 3.8 Validação de presença e tipo de cada campo obrigatório (`carta`, `nome`, `cima`) → `Erro(motivo="campo_faltando")` (GREEN)
- [x] 3.9 Commit: `test(04-protocolo): campo faltando vira erro` → `feat(04-protocolo): valida os campos obrigatórios de cada mensagem`

- [x] 3.10 Teste do cenário `nome é normalizado` (RED)
- [x] 3.11 `Entrar` normaliza o nome com `strip` antes de virar identidade (GREEN)
- [x] 3.12 Commit: `test(04-protocolo): nome é normalizado` → `feat(04-protocolo): normaliza o nome no codec`

- [x] 3.13 Teste do caso limite `EDGE - nome inválido vira erro` (RED)
- [x] 3.14 Guarda de 1 a 20 caracteres após o `strip` → `Erro(motivo="nome_invalido")` (GREEN)
- [x] 3.15 Commit: `test(04-protocolo): nome inválido vira erro` → `feat(04-protocolo): limita o nome a 20 caracteres`

- [x] 3.16 Teste do caso limite `EDGE - campo extra vira erro` (RED)
- [x] 3.17 Validação do conjunto exato de chaves de cada mensagem → `Erro(motivo="campo_extra")` (GREEN)
- [x] 3.18 Commit: `test(04-protocolo): campo extra vira erro` → `feat(04-protocolo): recusa campo desconhecido`

## 4. Teto de bytes por linha (RED → GREEN)

- [x] 4.1 Teste do caso limite `EDGE - linha acima do teto é fatal` (RED)
- [x] 4.2 `TETO_LINHA` (4096 bytes UTF-8, contando o `\n`, aplicado só na desserialização/leitura) e `LinhaLonga`, o único `raise` (GREEN)
- [x] 4.3 Commit: `test(04-protocolo): linha acima do teto é fatal` → `feat(04-protocolo): sinaliza a linha acima do teto`

- [x] 4.4 Teste do caso limite `EDGE - linha no limite é aceita` (RED esperado verde — cobre a fronteira `> TETO_LINHA` vs. `>=`; registrar como cobertura)
- [x] 4.5 Nenhuma implementação nova (GREEN)
- [x] 4.6 Commit: `test(04-protocolo): linha no limite é aceita`

- [x] 4.7 Teste do caso limite `EDGE - nenhum outro erro é fatal` (RED esperado verde — ancora a distinção `Erro` vs. `LinhaLonga`; registrar como cobertura)
- [x] 4.8 Nenhuma implementação nova (GREEN)
- [x] 4.9 Commit: `test(04-protocolo): nenhum outro erro é fatal`

## 5. Snapshot por assento (RED → GREEN)

- [x] 5.1 Teste do cenário `snapshot traz a própria mão` (RED)
- [x] 5.2 `Estado` (dataclass com todos os campos) e `estado(jogo, nomes, assento)` preenchendo `assentos` e `mao` com as cartas do assento (GREEN)
- [x] 5.3 Commit: `test(04-protocolo): snapshot traz a própria mão` → `feat(04-protocolo): adiciona o snapshot estado por assento`

- [x] 5.4 Teste do cenário `estado faz ida-e-volta` (RED)
- [x] 5.5 Codec do tipo `estado` no `serializar`/`desserializar` (GREEN)
- [x] 5.6 Commit: `test(04-protocolo): estado faz ida-e-volta` → `feat(04-protocolo): serializa o snapshot`

- [x] 5.7 Teste do caso limite `EDGE - snapshot traz só a contagem das outras mãos` (RED)
- [x] 5.8 `contagens` com o tamanho de cada mão; as mãos alheias não entram em campo algum (GREEN)
- [x] 5.9 Commit: `test(04-protocolo): snapshot traz só a contagem das outras mãos` → `feat(04-protocolo): mascara as mãos alheias no snapshot`

- [x] 5.10 Teste do caso limite `EDGE - snapshot reflete a mesa` (RED)
- [x] 5.11 `estado()` preenche `trunfo`, `carta_trunfo`, `vez`, `vaza`, `partidas`, `encerrado` e `vencedor` a partir do `Jogo` (GREEN)
- [x] 5.12 Commit: `test(04-protocolo): snapshot reflete a mesa` → `feat(04-protocolo): completa o snapshot com o estado do jogo`

- [x] 5.13 Teste do cenário `snapshot diz quem deve responder` (RED)
- [x] 5.14 `estado()` preenche `respondente` — `(embaralhador + 1) % 4` com a mão não preparada, `None` com a mão preparada (GREEN)
- [x] 5.15 Commit: `test(04-protocolo): snapshot diz quem deve responder` → `feat(04-protocolo): expõe quem responde cima ou baixo`

## 6. Erro de jogada formatado (RED → GREEN)

- [x] 6.1 Teste do caso limite `EDGE - jogada fora da vez vira erro` (RED)
- [x] 6.2 `erro_de_jogada(ErroJogada) -> Erro` com o mapa de motivos estáveis (GREEN)
- [x] 6.3 Commit: `test(04-protocolo): jogada fora da vez vira erro` → `feat(04-protocolo): formata o ErroJogada como erro`

- [x] 6.4 Teste do caso limite `EDGE - carta fora da mão vira erro` (RED esperado verde — mesmo mapa de 6.2; registrar como cobertura)
- [x] 6.5 Nenhuma implementação nova (GREEN)
- [x] 6.6 Commit: `test(04-protocolo): carta fora da mão vira erro`

- [x] 6.7 Teste do caso limite `EDGE - não seguir o naipe vira erro` (RED esperado verde — mesmo mapa de 6.2; registrar como cobertura)
- [x] 6.8 Nenhuma implementação nova (GREEN)
- [x] 6.9 Commit: `test(04-protocolo): não seguir o naipe vira erro`

## 7. Refatoração (apenas no GREEN)

- [x] 7.1 Refatorar `protocolo.py` mantendo todos os testes verdes (ex.: extrair a validação de shape de campo numa única função e o mapa `tipo → dataclass` num único ponto)
- [x] 7.2 Rodar a suite completa
- [x] 7.3 Commit: `refactor(04-protocolo): extrai a validação de campo e o despacho de tipo`

## 8. Validação Final

- [x] 8.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [x] 8.2 Tipos: `uv run mypy src`
- [x] 8.3 Suite completa uma última vez: `uv run pytest`
- [x] 8.4 Commit de ajustes finais: `style: aplica lint e formatação`

## 9. Retrabalho de verificação (RED → GREEN)

- [x] 9.1 Teste do cenário `erro faz ida-e-volta` (RED esperado verde — o codec do `erro` já existe; fecha as 3 linhas descobertas do relatório)
- [x] 9.2 Nenhuma implementação nova (GREEN)
- [x] 9.3 Commit: `test(04-protocolo): erro faz ida-e-volta`

- [x] 9.4 Teste do caso limite `EDGE - campo com tipo errado vira erro` (RED)
- [x] 9.5 `_validar`: campo com tipo errado passa a devolver `campo_invalido` em vez de `campo_faltando` (GREEN)
- [x] 9.6 Commit: `test(04-protocolo): campo com tipo errado vira erro` → `feat(04-protocolo): distingue campo_invalido de campo_faltando`

- [x] 9.7 Adicionar `pytest-cov` ao grupo `dev` do `pyproject.toml` e instalar (`uv sync`)
- [x] 9.8 Commit: `chore(04-protocolo): adiciona pytest-cov às dev-deps`

## 10. Layout: imagens para docs

- [x] 10.1 `git mv src/pysueca/imagens docs/imagens` e atualizar as referências em `AGENTS.md` (mapa de arquivos), `PLANO-PYSUECA-V1.md` ("Feito até agora") e `docs/adr/0004`
- [x] 10.2 Commit: `refactor(04-protocolo): move as imagens para docs/`

## 11. Validação Final (retrabalho)

- [x] 11.1 `AGENTS.md`: documenta `uv run pytest --cov=pysueca --cov-fail-under=80`
- [x] 11.2 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [x] 11.3 Tipos: `uv run mypy src`
- [x] 11.4 Suite com o gate: `uv run pytest --cov=pysueca --cov-fail-under=80`
- [ ] 11.5 Re-verificar e atualizar o relatório: `/pi-verificar`

## Notas de Execução

- **8.2/8.1 (pré-existentes, não regressões):** `uv run mypy src` continua com 1 erro (`main.py:52`, `App.dark`) e `uv run ruff check` com 4 (`main.py` RUF012 ×3 e `imagens/get_images.py` I001) — todos endereçados na sprint 06, que reescreve `main.py`. `protocolo.py` e `test_protocolo.py` passam limpos em `ruff check` e `ruff format --check`.
- **40→66 testes:** a suite fechou com 66 testes verdes (20 novos de `test_protocolo.py`); nenhuma regressão em `test_carta.py`/`test_motor.py`/`test_jogo.py`.
- **Correção de artefato (mascaramento):** o cenário `EDGE - snapshot traz só a contagem das outras mãos` falhou ao completar o snapshot com o trunfo — a **carta do trunfo é pública** (virada na mesa) e pode pertencer a outro assento, então o teste passou a ignorá-la no conjunto secreto (commit `test(04-protocolo): mascaramento ignora a carta pública do trunfo`). Sem isso, o teste rejeitaria um snapshot correto.
- **RED esperado verde (cobertura) e commits agrupados:** 4.4 e 4.7 são fronteiras da mesma guarda de 4.2 e fecharam no commit `test(04-protocolo): linha no limite é aceita e nenhum outro erro é fatal`; 6.4 e 6.7 são o mesmo mapa de 6.2 e fecharam como cobertura (commits `test(...)`, sem `feat`).
- **Ordem RED→GREEN do `estado faz ida-e-volta`:** o codec do `Estado` chegou a ser escrito antes do teste; foi revertido (`git checkout`), o teste entrou como RED genuíno e só então o `feat` voltou.
- **8.4:** `ruff format` aplicado só em `protocolo.py` e `test_protocolo.py` (os dois arquivos da sprint); `main.py`/`get_images.py` intocados.

## Notas de Execução (retrabalho da verificação)

- **9.1/9.2 (RED esperado verde):** o codec do `erro` já existia (fases 1–8); o teste `erro_faz_ida_e_volta` fechou as 3 linhas descobertas do relatório (`_para_dados` do `erro`, `return Erro(dados["motivo"])`) — `protocolo.py` foi de 97,9% para **100%**.
- **9.4/9.5 (RED genuíno):** o teste de campo com tipo errado falhou com `campo_faltando` antes de o `_validar` passar a devolver `campo_invalido`.
- **9.7:** `pytest-cov 7.1.0` (+ `coverage 7.16.2`) no grupo `dev`; `pyproject.toml` e `uv.lock` atualizados.
- **10.1:** `git mv` de 41 arquivos (`docs/imagens/`), com as referências de `AGENTS.md`, `PLANO-PYSUECA-V1.md` e `docs/adr/0004` no mesmo commit. Os relatórios históricos das sprints 01–03 e os `design.md`/`tasks.md` antigos citam o caminho velho de propósito (registro da época).
- **11.1 (além do comando):** o `AGENTS.md` tinha o mapa desatualizado desde a sprint 02 — `motor.py` e `protocolo.py` não constavam — e a invariante ainda dizia "o futuro `motor.py`"; corrigidos junto do comando do gate.
- **11.4:** `uv run pytest --cov=pysueca --cov-fail-under=80` → `93.63%` (gate de 80% atingido). `protocolo.py`, `motor.py`, `carta.py` e `baralho.py` em 100%; `main.py` em 0% (pré-existente, reescrita na sprint 06) e `__init__.py` em 50%.
- **11.2/11.3 (pré-existentes, não regressões):** `uv run ruff check` acusa 4 erros — `main.py:14,21,28` (RUF012) e `docs/imagens/get_images.py:1` (I001, agora no caminho novo) — e `uv run mypy src` acusa 1 (`main.py:52`). Todos endereçados na sprint 06. `protocolo.py` e `test_protocolo.py` limpos em `ruff check` e `ruff format --check`.
- **11.5:** é o handoff para `/pi-verificar` (o `advance sprint-verificacao` fecha esta sprint); fica aberto aqui de propósito.

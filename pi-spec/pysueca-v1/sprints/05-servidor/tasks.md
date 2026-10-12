# Tasks — Sprint 05 — Servidor

> **Sprint:** `sprints/05-servidor/` — rastreia `sprints/05-servidor/qa-plan.md`, `sprints/05-servidor/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [x] 1.1 Criar branch `feat/pysueca-v1-05-servidor` — scope `05-servidor` nos commits
- [x] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 05-servidor — servidor` (`sprints/05-servidor/*.md` + `specs/**`)

## 2. Servidor mínimo: entrada e assento (tracer bullet, RED → GREEN)

- [ ] 2.1 Teste do cenário `entrar senta no primeiro assento livre` (RED) — sobe o servidor em `127.0.0.1:0` com `asyncio.run(cenario())` e um helper de conectar/ler linha
- [ ] 2.2 `src/pysueca/servidor.py`: `Servidor` (que **é** a mesa: `nomes`, `conexoes`, `Jogo`), `async def iniciar(host, porta) -> asyncio.Server` (`asyncio.start_server(..., limit=TETO_LINHA)`) e `atender` com `entrar` → primeiro assento livre + snapshot por assento (GREEN)
- [ ] 2.3 Commit: `test(05-servidor): entrar senta no primeiro assento livre` → `feat(05-servidor): sobe o servidor TCP e senta o primeiro assento`

## 3. Erros de assento (RED → GREEN)

- [ ] 3.1 Teste do caso limite `EDGE - nome já sentado e ativo é recusado` (RED)
- [ ] 3.2 Guarda de `nome_em_uso` — só conexão viva bloqueia; assento reservado não (GREEN)
- [ ] 3.3 Commit: `test(05-servidor): nome já sentado e ativo é recusado` → `feat(05-servidor): recusa nome em uso`

- [ ] 3.4 Teste do caso limite `EDGE - mesa cheia recusa o quinto` (RED)
- [ ] 3.5 Guarda de `mesa_cheia` — sem assento livre e sem nome reservado correspondente (GREEN)
- [ ] 3.6 Commit: `test(05-servidor): mesa cheia recusa o quinto` → `feat(05-servidor): recusa a quinta conexão`

- [ ] 3.7 Teste do caso limite `EDGE - não sentado é recusado` (RED)
- [ ] 3.8 Guarda de `nao_sentado` para `jogar`/`responder` de conexão sem assento (GREEN)
- [ ] 3.9 Commit: `test(05-servidor): não sentado é recusado` → `feat(05-servidor): exige assento antes de agir`

- [ ] 3.10 Teste do caso limite `EDGE - mensagem de direção errada é recusada` (RED)
- [ ] 3.11 Guarda de `mensagem_invalida` para `estado`/`erro` vindos de cliente no despacho (GREEN)
- [ ] 3.12 Commit: `test(05-servidor): mensagem de direção errada é recusada` → `feat(05-servidor): recusa estado e erro vindos de cliente`

## 4. Início da mão: cima ou baixo (RED → GREEN)

- [ ] 4.1 Teste do cenário `quatro assentos abrem a pergunta cima ou baixo` (RED)
- [ ] 4.2 Broadcast do snapshot a cada assento ocupado, com `respondente` do parceiro do dador (GREEN)
- [ ] 4.3 Commit: `test(05-servidor): quatro assentos abrem a pergunta cima ou baixo` → `feat(05-servidor): transmite o snapshot a cada assento ocupado`

- [ ] 4.4 Teste do cenário `responder prepara a mão e distribui dez cartas` (RED)
- [ ] 4.5 `responder` do assento certo chama `Jogo.preparar(cima)` e broadcasta as dez cartas (GREEN)
- [ ] 4.6 Commit: `test(05-servidor): responder prepara a mão e distribui dez cartas` → `feat(05-servidor): prepara a mão pela resposta cima ou baixo`

- [ ] 4.7 Teste do caso limite `EDGE - responder fora de hora é recusado` (RED)
- [ ] 4.8 Guarda de `mesa_incompleta` (menos de quatro assentos) e de `responder` de quem não é o respondente ou com a mão preparada (GREEN)
- [ ] 4.9 Commit: `test(05-servidor): responder fora de hora é recusado` → `feat(05-servidor): recusa resposta fora de hora`

## 5. Jogada pelo motor e contagem da mão (RED → GREEN)

- [ ] 5.1 Teste do cenário `jogada ilegal vira erro só para quem jogou` (RED)
- [ ] 5.2 `jogar` chama `Jogo.jogar` e traduz o `ErroJogada` com `erro_de_jogada`, endereçado só à conexão que jogou (GREEN)
- [ ] 5.3 Commit: `test(05-servidor): jogada ilegal vira erro só para quem jogou` → `feat(05-servidor): recusa a jogada ilegal pelo motor`

- [ ] 5.4 Teste do cenário `jogada legal chega aos quatro` (RED)
- [ ] 5.5 Broadcast do snapshot novo depois da jogada legal (GREEN)
- [ ] 5.6 Commit: `test(05-servidor): jogada legal chega aos quatro` → `feat(05-servidor): transmite a jogada legal`

- [ ] 5.7 Teste do cenário `a décima vaza conta a mão` (RED) — quatro robôs com `random.Random(seed)` e `jogada_legal` (`motor.py:21`) escolhendo a carta; asserção por invariante (120 pontos, partidas coerentes com o `Resultado`, quatro mãos vazias), não pelo placar congelado
- [ ] 5.8 `VAZAS_POR_MAO = 10` e `encerrar_mao` quando a décima vaza fecha; broadcast do placar (GREEN)
- [ ] 5.9 Commit: `test(05-servidor): a décima vaza conta a mão` → `feat(05-servidor): conta a mão ao fechar a décima vaza`

- [ ] 5.10 Teste do caso limite `EDGE - mão nova volta a perguntar cima ou baixo` (RED esperado verde — o caminho do 4.2 cobre a mão nova; registrar como cobertura)
- [ ] 5.11 Nenhuma implementação nova (GREEN)
- [ ] 5.12 Commit: `test(05-servidor): mão nova volta a perguntar cima ou baixo`

- [ ] 5.13 Teste do cenário `o jogo encerrado não abre mão nova` (RED) — os robôs jogam a série até a quarta partida com `random.Random(seed)`
- [ ] 5.14 `encerrar_mao` sem abrir mão nova quando o jogo encerra; snapshot final com `encerrado`/`vencedor` e as conexões de pé (GREEN)
- [ ] 5.15 Commit: `test(05-servidor): o jogo encerrado não abre mão nova` → `feat(05-servidor): transmite o placar final e para de distribuir`

## 6. Queda, reserva e reconexão (RED → GREEN)

- [ ] 6.1 Teste do cenário `queda congela a mesa e avisa os outros três` (RED)
- [ ] 6.2 `Estado.ausentes: list[int]` no `protocolo.py`: campo, serialização, `_CAMPOS["estado"]` e o ramo de `desserializar`, mais a cobertura do ida-e-volta do `estado` (GREEN)
- [ ] 6.3 Commit: `test(05-servidor): queda congela a mesa e avisa os outros três` → `feat(05-servidor): anuncia a queda no snapshot e reserva o assento`

- [ ] 6.4 Teste do caso limite `EDGE - mesa congelada recusa jogadas` (RED)
- [ ] 6.5 Guarda de `mesa_congelada` para `jogar`/`responder` com assento ausente (GREEN)
- [ ] 6.6 Commit: `test(05-servidor): mesa congelada recusa jogadas` → `feat(05-servidor): congela a mesa enquanto falta um assento`

- [ ] 6.7 Teste do cenário `reconexão com o mesmo nome retoma o assento` (RED)
- [ ] 6.8 `entrar` com nome reservado retoma o assento, sai de `ausentes` e descongela; broadcast (GREEN)
- [ ] 6.9 Commit: `test(05-servidor): reconexão com o mesmo nome retoma o assento` → `feat(05-servidor): devolve o assento reservado ao dono`

- [ ] 6.10 Teste do caso limite `EDGE - estado carrega os assentos ausentes` (protocolo) (RED esperado verde — o campo entrou em 6.2; registrar como cobertura)
- [ ] 6.11 Nenhuma implementação nova (GREEN)
- [ ] 6.12 Commit: `test(05-servidor): estado carrega os assentos ausentes`

- [ ] 6.13 Teste do caso limite `EDGE - ausentes com tipo errado vira erro` (RED esperado verde — o `_CAMPOS` de 6.2 já valida o tipo; registrar como cobertura)
- [ ] 6.14 Nenhuma implementação nova (GREEN)
- [ ] 6.15 Commit: `test(05-servidor): ausentes com tipo errado vira erro`

## 7. Teto de bytes fecha só aquela conexão (RED → GREEN)

- [ ] 7.1 Teste do cenário `linha acima do teto fecha aquela conexão` (RED)
- [ ] 7.2 `limit=TETO_LINHA` em `start_server` e o `ValueError`/`LinhaLonga` do `readline` convergindo no mesmo `finally` da queda (GREEN)
- [ ] 7.3 Commit: `test(05-servidor): linha acima do teto fecha aquela conexão` → `feat(05-servidor): fecha só a conexão acima do teto`

- [ ] 7.4 Teste do caso limite `EDGE - os outros três seguem na mesa` (RED esperado verde — mesmo `finally` de 7.2; registrar como cobertura)
- [ ] 7.5 Nenhuma implementação nova (GREEN)
- [ ] 7.6 Commit: `test(05-servidor): os outros três seguem na mesa`

## 8. Refatoração (apenas no GREEN)

- [ ] 8.1 Refatorar `servidor.py` mantendo todos os testes verdes (ex.: isolar o envio de `Erro` e o broadcast de snapshot em funções únicas, tirar do handler qualquer regra de assento)
- [ ] 8.2 Rodar a suite completa
- [ ] 8.3 Commit: `refactor(05-servidor): isola o broadcast e o erro de assento`

## 9. Documentação

- [ ] 9.1 `AGENTS.md`: `src/pysueca/servidor.py` no mapa de arquivos (assentos, intenções pelo motor, broadcast e queda) e a invariante de que só ele usa `asyncio`/rede
- [ ] 9.2 Commit: `docs(05-servidor): documenta o servidor e a invariante da casca asyncio`

## 10. Validação Final

- [ ] 10.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [ ] 10.2 Tipos: `uv run mypy src`
- [ ] 10.3 Suite completa uma última vez: `uv run pytest`
- [ ] 10.4 Gate de cobertura: `uv run pytest --cov=pysueca --cov-fail-under=80`
- [ ] 10.5 Commit de ajustes finais: `style: aplica lint e formatação`

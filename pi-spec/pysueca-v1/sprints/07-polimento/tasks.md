# Tasks — Sprint 07 — Polimento

> **Sprint:** `sprints/07-polimento/` — rastreia `sprints/07-polimento/qa-plan.md`, `sprints/07-polimento/specs/<cap>/spec.md` e `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## 1. Configuração Git e Planejamento

- [x] 1.1 Criar branch `feat/pysueca-v1-07-polimento` — scope `07-polimento` nos commits
- [x] 1.2 Commit dos artefatos de planejamento: `docs(planejamento): sprint 07-polimento — polimento` (`sprints/07-polimento/*.md` + `specs/**`)

## 2. Avisos em linguagem de jogador (tracer bullet, RED → GREEN)

- [x] 2.1 Teste `todo código de motivo do v1 vira frase de jogador` (RED) — função pura de tela (`frase_do_motivo`), percorrendo os três `ErroJogada`, os motivos do servidor e os da forma do fio; hoje nenhuma frase existe
- [x] 2.2 `MOTIVOS` (todos os códigos do v1) e `frase_do_motivo` em `src/pysueca/main.py`, com `avisar` passando o motivo pela tradução antes de guardar no `aviso_erro`; o motivo de estado é fraseado pela ação recusada (GREEN; decisões 1, 2, 9 e 13)
- [x] 2.3 Commit: `test(07-polimento): todo código de motivo do v1 vira frase de jogador` → `feat(07-polimento): traduz o motivo de recusa para a tela`

- [x] 2.4 Teste `o nome em uso vira frase na tela` (RED) — o assert de `tests/test_cliente.py:477-481` troca `nome_em_uso` pela frase e a ausência do código; o mesmo vale para o `fora_de_hora` de `tests/test_cliente.py:319-321`, no teste `EDGE - o erro do servidor aparece como frase` do qa-plan
- [x] 2.5 Nenhuma implementação nova: `frase_do_motivo` de 2.2 já cobre o `_traduzir`/`avisar` inteiro (GREEN)
- [x] 2.6 Commit: `test(07-polimento): o nome em uso vira frase na tela`

- [x] 2.7 Teste `EDGE - o JSON inválido vira frase` (RED) — o assert de `tests/test_cliente.py:490-493` troca `json_invalido` pela frase
- [x] 2.8 Nenhuma implementação nova (GREEN; cobertura declarada: o motivo local passa pelo mesmo `avisar`)
- [x] 2.9 Commit: `test(07-polimento): o JSON inválido vira frase`

- [x] 2.10 Teste `EDGE - motivo desconhecido não vaza código nem derruba a tela` (RED) — `frase_do_motivo("bug_novo")` e um `erro` com motivo fora do dicionário
- [x] 2.11 Fallback genérico no `frase_do_motivo` (GREEN; decisão 2: frase genérica pura, sem o código)
- [x] 2.12 Commit: `test(07-polimento): motivo desconhecido não vaza código` → `feat(07-polimento): cai na frase genérica para motivo não previsto`

## 3. Fim de jogo na mesa (RED → GREEN)

- [x] 3.1 Teste `o fim do jogo aparece na mesa` (RED) — `desenhar_mesa` com `encerrado=True`, `partidas=[4, 2]`, `vencedor=0`
- [x] 3.2 `desenhar_mesa` ganha a linha de fim de jogo com o placar final e a dupla vencedora nomeada quando os dois nomes existem em `assentos`, caindo para `dupla 0–2`/`dupla 1–3` (GREEN; decisões 3 e 10)
- [x] 3.3 Commit: `test(07-polimento): o fim do jogo aparece na mesa` → `feat(07-polimento): desenha o fim de jogo e a dupla vencedora`

- [x] 3.4 Teste `a mesa encerrada não anuncia vez` (RED) — `texto_aviso` com `encerrado=True` e `vez` no assento do jogador
- [x] 3.5 `texto_aviso` ignora a vez com `encerrado` (GREEN; decisão 4)
- [x] 3.6 Commit: `test(07-polimento): a mesa encerrada não anuncia vez` → `feat(07-polimento): silencia a vez no fim do jogo`

- [x] 3.7 Teste `EDGE - o jogo em andamento segue mostrando o placar simples` (RED esperado verde — é o ramo de `desenhar_mesa` que a 06 já cobre; registrar como cobertura)
- [x] 3.8 Nenhuma implementação nova (GREEN)
- [x] 3.9 Commit: `test(07-polimento): o jogo em andamento segue mostrando o placar simples`

- [x] 3.10 Teste `a mesa encerrada não manda jogar` (RED) — `Enter` com `encerrado` verdadeiro e a mão cheia
- [x] 3.11 `action_jogar` (`main.py:200-202`) soma `estado.encerrado` ao guard de mão vazia (GREEN; decisão 12)
- [x] 3.12 Commit: `test(07-polimento): a mesa encerrada não manda jogar` → `feat(07-polimento): silencia a tecla de jogar no fim do jogo`

- [x] 3.13 Teste `EDGE - o nome ausente cai para a dupla` (RED esperado verde — é o ramo do fallback de 3.2; registrar como cobertura)
- [x] 3.14 Nenhuma implementação nova (GREEN)
- [x] 3.15 Commit: `test(07-polimento): o nome ausente cai para a dupla`

## 4. Teclas no rodapé e tema (RED → GREEN)

- [x] 4.1 Teste `as teclas de jogo aparecem no rodapé` (RED) — `app.query(FooterKey)` com `(tecla, descrição)` visíveis
- [x] 4.2 `main.py:115-117`: as três teclas de jogo perdem `show=False` (GREEN; decisão 5)
- [x] 4.3 Commit: `test(07-polimento): as teclas de jogo aparecem no rodapé` → `feat(07-polimento): mostra as teclas de jogo no rodapé`

- [x] 4.4 Teste `d alterna o tema` (RED) — `Binding("d", "toggle_dark", …)` e `app.theme` trocando entre `textual-dark` e `textual-light`
- [x] 4.5 O binding `d` volta ao `BINDINGS` da `SuecaApp` apontando para o `action_toggle_dark` do Textual, visível no rodapé com a descrição `Tema` (GREEN; decisões 6 e 11)
- [x] 4.6 Commit: `test(07-polimento): d alterna o tema` → `feat(07-polimento): devolve o tema claro e escuro à tecla d`

- [x] 4.7 Teste `EDGE - o tema não muda a cor do naipe` (RED esperado verde — o markup fixo vem da 06, task 3.2; registrar como cobertura)
- [x] 4.8 Nenhuma implementação nova (GREEN)
- [x] 4.9 Commit: `test(07-polimento): o tema não muda a cor do naipe`

## 5. Recusa com a mesa congelada (RED → GREEN)

- [x] 5.1 Teste `congelado, a recusa do servidor vira frase de jogador` (RED) — o assert de `tests/test_cliente.py:551-553` troca `mesa_congelada` pela frase
- [x] 5.2 Nenhuma implementação nova além da prioridade do `#aviso` que o grill decidiu manter (GREEN; decisão 9: a frase da ação convive com o banner do estado, sem dedup)
- [x] 5.3 Commit: `test(07-polimento): congelado, a recusa vira frase de jogador`

- [x] 5.4 Teste `EDGE - o erro do servidor aparece como frase` (RED esperado verde — mesmo ramo de `o nome em uso vira frase na tela`; cobertura declarada)
- [x] 5.5 Nenhuma implementação nova (GREEN)
- [x] 5.6 Commit: `test(07-polimento): o erro do servidor aparece como frase`

## 6. README: o v1 pronto e duas máquinas

- [x] 6.1 `README.md:64-81`: manter o roteiro de quatro terminais e acrescentar o passo a passo entre duas máquinas (`pysueca-servidor --host 0.0.0.0`, clientes com `--host <ip>`, o comando que descobre o endereço da máquina e o aviso de firewall) e a declaração do que o v1 entrega e do que fica fora (GREEN; decisão 8; o comando do IP fica delegado à implementação, decisão 14)
- [x] 6.2 Commit: `docs(07-polimento): o v1 pronto e o passo a passo de duas máquinas`

## 7. Refatoração (apenas no GREEN)

- [x] 7.1 Refatorar `main.py` mantendo todos os testes verdes (ex.: separar o texto do fim de jogo e a tabela `MOTIVOS` do corpo de `desenhar_mesa`/`avisar`)
- [x] 7.2 Rodar a suite completa
- [x] 7.3 Commit: `refactor(07-polimento): isola o fim de jogo e a tabela de motivos`

## 8. Documentação

- [x] 8.1 `AGENTS.md`: o mapa de `src/pysueca/main.py` cita o `MOTIVOS`, o fim de jogo e as teclas; a linha do `README.md` deixa de ser só o roteiro e passa a incluir o v1 pronto e duas máquinas
- [x] 8.2 Commit: `docs(07-polimento): documenta o polimento da tela`

## 9. Validação Final

- [x] 9.1 Lint e formatação: `uv run ruff check` e `uv run ruff format --check`
- [x] 9.2 Tipos: `uv run mypy src`
- [x] 9.3 Suite completa uma última vez: `uv run pytest`
- [x] 9.4 Gate de cobertura: `uv run pytest --cov=pysueca --cov-fail-under=80`
- [x] 9.5 Leitura manual do `README.md`: roteiro de quatro terminais e passo a passo de duas máquinas conferidos à mão
- [ ] 9.6 Roteiro manual de 4 terminais conferido à mão: uma mão completa com a mesa em fim de jogo na tela
- [x] 9.7 Commit de ajustes finais: `style: aplica lint e formatação`

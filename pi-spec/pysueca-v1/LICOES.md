# Lições Aprendidas — PYSUECA-V1

> **Iniciativa:** `pi-spec/pysueca-v1/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> Arquivo append-only — cada sprint acrescenta uma seção ao final. Nunca sobrescreva.

---

## Sprint 01-carta-e-baralho — Carta e baralho — 2026-10-12

**Aprendizado:** a aritmética de carta fechou numa tabela única em `Valor` (`pontos`/`forca` como dados do enum), e a assinatura `vence(outra, naipe_puxado, trunfo)` foi decidida antes de codar — o grill pegou o furo do vaza de três naipes (descarte de força maior vencendo o naipe puxado). Por outro lado, `carta.py` nasceu completo demais: 4 cenários (pontos, força, texto) não chegaram a ficar vermelhos, viraram só cobertura.

**O que muda nas próximas sprints:** escrever a 1ª versão do módulo com o mínimo que faz o tracer bullet passar (ex.: `Naipe`/`Valor` sem `pontos`/`forca`/`de_texto`) e adicionar cada campo no seu ciclo RED→GREEN, para todo cenário do qa-plan ter um vermelho de verdade.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste do guard de tamanho de `de_texto` (`carta.py:80`) | baixa | ramo defensivo de 1 linha; cobrir no próximo teste de `carta.py` |
| Teste de `Carta.__str__` (`carta.py:75`) | baixa | sem consumidor até a sprint 06; cobrir quando a TUI usar |

**Evidências:** `pi-spec/pysueca-v1/execucao/01-carta-e-baralho/relatorio-verificacao.md`

---

## Sprint 01-carta-e-baralho — Re-verificação (retrabalho) — 2026-10-12

**Aprendizado:** os dois gaps de cobertura da primeira verificação fecharam num ciclo curto, sem mudar comportamento: `Carta.__str__` saiu (YAGNI, sem consumidor) e o guard de tamanho de `de_texto` ganhou EDGE (`"7HH"`/`"7"`/`""` → `ValueError`). `carta.py` e `baralho.py` ficaram em 100% de cobertura.

**O que muda nas próximas sprints:** retrabalho de verificação deve ficar restrito a teste/limpeza quando o motor já está correto; o ciclo `grill → atualizar → implementar → verificar` reabre sem atrito.

**Retrabalho adiado:** nenhum desta sprint. Resta só `uv run mypy src` vermelho por `main.py:52` (pré-existente), endereçado na sprint 06 que reescreve `main.py`.

**Evidências:** `pi-spec/pysueca-v1/execucao/01-carta-e-baralho/relatorio-verificacao.md`

---

## Sprint 02-vaza-e-mao — Vaza e mão — 2026-10-12

**Aprendizado:** a `Mao` como máquina de estados explícita (`preparar` → 10 vazas → `pontos`/`resultado`) fechou com 100% de cobertura de `motor.py` e sem reimplementar precedência — `Vaza.vencedor` só agrega `Carta.vence`, então os cenários de desempate (trunfo, entre trunfos, descarte) nasceram verdes. O refactor `_validar` (task 7.1) tornou explícito o invariante "validar tudo antes de mutar" e sustenta o EDGE "jogada ilegal não altera o estado". O que **não** funcionou: de novo o módulo cresceu antes do 1º vermelho — os cenários `4.7` (trunfar sem o naipe) e `5.4` (quilo/bandeira) foram marcados RED, mas a implementação adjacente já os cobria e eles viraram só cobertura, repetindo a lição da sprint 01.

**O que muda nas próximas sprints:** implementar exatamente o ramo que o teste pede e deixar o outro ramo para o próximo RED — em `jogada_legal`, o 1º GREEN deveria ter sido `return carta.naipe is naipe_puxado` (recusa o outro naipe) e o ramo "mão sem o naipe → libera" só vir no teste 4.7; em `Resultado.de_pontos`, o 1º GREEN só com empate/normal e os limites 91/119/120 no teste 5.4. Reduzir o escopo do `feat(...)` ao mínimo que faz o teste atual passar.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Registrar/reforçar o vício de "RED esperado verde" por implementação antecipada (4.7, 5.4) | média | reduz o sinal dos testes das sprints 03–06; virou padrão recorrente desde a sprint 01 |
| Atualizar a linha de decisão arquitetural do PLANO (`puxar` fundido em `Mao.jogar`, decisão 2 do `design.md`) | baixa | leitura do PLANO diverge do design; sem custo de execução |
| Fechar `mypy src` (`main.py:52`) e `ruff check` (`main.py` RUF012, `imagens/get_images.py` I001) | baixa | pré-existentes, endereçados na sprint 06 que reescreve `main.py` |

**Evidências:** `pi-spec/pysueca-v1/execucao/02-vaza-e-mao/relatorio-verificacao.md`

---

## Sprint 03-jogo-e-papeis — Jogo e papéis — 2026-10-12

**Aprendizado:** o `Jogo` fechou como dono único da mesa (`preparar`/`jogar`/`encerrar_mao` + placar + `encerrado`/`vencedor`) reaproveitando `Mao`/`Vaza` sem tocar na sprint 02 — `motor.py` ficou em 99% de cobertura e `test_jogo.py` com 11 testes. O RED fez o seu trabalho de verdade uma vez: o teste de quilo (`test_quilo_soma_duas_partidas_a_dupla_1`) **falhou** porque o próprio `qa-plan.md` trazia `41 a 79`, que é vitória normal, não quilo; o vermelho revelou o defeito do artefato antes de virar código errado (`29 a 91` é quilo). O que de novo **não** funcionou: repetiu-se o "RED esperado verde" (tasks 2.4, 4.4, 4.7, 6.4, 6.7), agora explícito no `tasks.md` como cobertura — sinal de teste ainda fraco na 3ª sprint seguida.

**O que muda nas próximas sprints:** tratar os cenários de cobertura declarados no `qa-plan.md` como EDGE de ramo (não como RED independente) e, ao escrever o teste, cobrir de fato o ramo novo — o cenário de empate 60–60 só ficou observável depois de receber as asserções de rotação (`5.1`) e `encerrado is False` (`6.1`), que ficaram vermelhas junto do seu GREEN. Sempre que um teste de placar falhar, desconfiar primeiro da aritmética do artefato (soma 120, faixa 91–119 para quilo).

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (`motor.py:183`, única linha descoberta) | baixa | contrato documentado sem teste; protocolo (04) e TUI (06) trazem seus próprios testes |
| `ruff`/`mypy` vermelhos em `main.py` e `imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na sprint 06 |

**Evidências:** `pi-spec/pysueca-v1/execucao/03-jogo-e-papeis/relatorio-verificacao.md`

---

## Sprint 04-protocolo — Protocolo — 2026-10-12

**Aprendizado:** o `protocolo.py` fechou com 20 testes e 97,9% de cobertura sem tocar o motor — a fronteira fixada na sprint 02 (erros de regra no motor, erros de fio no protocolo) sustentou a implementação: `erro_de_jogada` virou `Erro(erro.value)` porque o `ErroJogada` já carregava o identificador de fio, e nenhuma checagem de vez/posse/naipe foi duplicada. O RED funcionou de novo como auditor de artefato: o teste de mascaramento reprovou um snapshot **correto** porque a carta do trunfo é pública (virada na mesa) e pode estar na mão de outro assento — o `qa-plan.md` ("nenhuma carta alheia em campo algum") é que estava errado, e o teste passou a ignorar a carta pública. O que **não** funcionou: o codec do `Estado` foi escrito antes do teste de ida-e-volta (revertido com `git checkout` para virar RED genuíno) e o `feat` de `estado()` deixou a suite vermelha por interagir com uma asserção antiga do teste de mascaramento, corrigida em commit seguinte em vez de dentro do mesmo ciclo.

**O que muda nas próximas sprints:** cenário de mascaramento precisa declarar explicitamente o que é secreto — "tudo menos a minha mão" é falso quando há informação pública no snapshot (trunfo); e ao completar um campo do snapshot, rodar a suite **antes** de commitar o `feat`, porque o efeito cruzado entre campo novo e teste antigo foi o que quebrou o verde.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste de ida-e-volta de `erro` (serializar + desserializar) | média | caminho de saída da 05 sem teste; 3 linhas descobertas, 1 por sentido |
| Teste de campo com tipo errado em `_validar` | baixa | ramo defensivo de 1 linha; o caminho de campo faltando o exercita parcialmente |
| `pytest-cov` nas dev-deps (cobertura hoje via `trace`) | baixa | medição manual a cada verificação |
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (arrastado da sprint 03) | baixa | contrato documentado sem teste; protocolo (04) e TUI (06) trazem os seus |
| `ruff`/`mypy` vermelhos em `main.py` e `imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na sprint 06 |

**Evidências:** `pi-spec/pysueca-v1/execucao/04-protocolo/relatorio-verificacao.md`

---

## Sprint 04-protocolo — Re-verificação (retrabalho) — 2026-10-12

**Aprendizado:** o retrabalho fechou os 3 itens do primeiro parecer num ciclo curto e sem mudar arquitetura: `campo_invalido` separou "tipo errado" de "ausente" com um RED genuíno, e o teste de ida-e-volta do `erro` levou `protocolo.py` a 100%. O `pytest-cov` + gate de 80% só ficou limpo junto do `git mv` das imagens para `docs/` — tirando `get_images.py` de dentro do pacote, `--cov=pysueca` deixa de medir um script sem teste. O gate global passou com folga (93,6%) mesmo com `main.py` em 0%.

**O que muda nas próximas sprints:** a cobertura passa a ser medida por `uv run pytest --cov=pysueca --cov-fail-under=80` (documentado no `AGENTS.md`); qualquer módulo novo que derrube o pacote abaixo de 80% falha o gate — a TUI (06) precisa manter `main.py` coberto ao reescrevê-lo.

**Retrabalho adiado:** nenhum desta re-verificação.

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| `__init__.py` em 50% de cobertura | baixa | linha de versão não exercitada; sem caminho de jogo |
| `ruff`/`mypy` pré-existentes em `main.py` e `docs/imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na sprint 06 |
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (arrastado da sprint 03) | baixa | contrato documentado sem teste; protocolo (04) e TUI (06) trazem os seus |

**Evidências:** `pi-spec/pysueca-v1/execucao/04-protocolo/relatorio-verificacao.md`

---

## Sprint 05-servidor — Servidor — 2026-10-12

**Aprendizado:** o `servidor.py` fechou com 18 testes de cliente real e 100% de cobertura sem tocar o motor — a fronteira "o motor decide, o protocolo formata, a casca só conecta" sustentou tudo: `_jogar` chama `Jogo.jogar` e traduz o `ErroJogada`, nenhuma regra de vez/posse/naipe repetida. O RED de novo auditou o teste, não a implementação: `drenar` engolia broadcasts anteriores e "os quatro recebem a própria mão com nove cartas" só vale para quem jogou — as duas asserções erradas foram corrigidas dentro do ciclo, antes de commitar o `feat`. O `asyncio` cobrou dois pedágios: `Server.wait_closed()` espera handlers e transportes, então fechar o `escritor` no `finally` e não esperar `wait_closed` no teardown destravou a suite; e o `ValueError` do `readline` acima do teto escapava da task (registrado no loop), resolvido com o mesmo `break`/`finally` da queda. O desvio do motivo `fora_de_hora` (ausente na decisão 8) foi dobrado de volta no `design.md` e no `spec.md` durante a verificação, mantendo a cadeia PLANO → spec → qa-plan → tasks honesta.

**O que muda nas próximas sprints:** teste de servidor precisa de leitura determinística — um `receber` por broadcast em vez de drenar até timeout; e todo caminho de leitura de socket (EOF, reset, teto) tem de terminar no mesmo `finally`, sem exceção escapando para o loop.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Motivo `fora_de_hora` — incorporado à decisão 8 do `design.md` e ao `spec.md` na verificação | baixa | resolvido; rastreabilidade fechada, sem retrabalho |
| `ruff`/`mypy` pré-existentes em `main.py` e `docs/imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na 06 |
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (arrastado da 03/04) | baixa | contrato documentado sem teste; protocolo e TUI trazem os seus |

**Evidências:** `pi-spec/pysueca-v1/execucao/05-servidor/relatorio-verificacao.md`

---

## Sprint 06-cliente-tui — Cliente TUI — 2026-10-12

**Aprendizado:** o cliente fechou com 25 testes e 94% de `main.py` sem tocar o motor, o protocolo nem a mesa — a fronteira "só o worker importa `protocolo`, nenhum widget conhece o fio" sustentou tudo: `_traduzir` é o único ponto de tradução e `mostrar_estado` é uma função do snapshot. O servidor falso roteirizado, falando o codec real (`serializar`/`desserializar`), provou o fio nos dois sentidos sem acoplar a TUI ao motor. Duas técnicas fizeram o teste da tela determinístico: `aguardar(pilot, condição)` num laço de `pilot.pause()` (sem `sleep`) para eventos de socket, e a leitura da tela por `Static.render().plain`/`spans`, nunca pelo tipo `Estado`. O RED genuíno só existiu quando o código foi de fato revertido (5.5, 5.8, 6.13 e o ImportError da 7.4); a maioria das tasks marcadas RED já estava coberta por implementação anterior (clamp de 4.2, `avisar` de 4.8, `meu_assento` de 5.2, `argparse` do tracer bullet) — repetição da lição das sprints 01–05.

**O que muda nas próximas sprints:** no qa-plan, declarar "cobertura de ramo" em vez de RED quando a implementação vizinha já cobre; no código, implementar cada ramo só no seu ciclo (o `argparse` e a `RespostaScreen` nasceram no tracer bullet e viraram cobertura). Em teste de TUI: usar o laço de `pause` para eventos de socket e ler a tela renderizada.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste do `b` → `Responder(False)` (`main.py:101` descoberta) | média | requisito da spec sem prova; ramo simétrico ao `c` |
| Guard da seleção com mão vazia, EOF/`finally`/aviso de fim de conexão, `meu_assento` ausente, `main()` das fachadas e casos-limite (vaza vazia/cheia, `None` no meio, `encerrado`) | baixa | ramos defensivos/fachada; sem caminho de jogo quebrado |
| `ConnectionResetError` em `Servidor._desconectar` (arrastado da 05) | baixa | só o fechamento abrupto do cliente dispara; o worker fecha de forma limpa |
| `ruff`/`mypy` de `docs/imagens/get_images.py` | baixa | resolvido nesta sprint (lint/format aplicados) |

**Evidências:** `pi-spec/pysueca-v1/execucao/06-cliente-tui/relatorio-verificacao.md`

---

## Sprint 06-cliente-tui — Re-verificação (retrabalho) — 2026-10-12

**Aprendizado:** o retrabalho fechou a lacuna média do `b` e os ramos de cobertura do cliente em seis ciclos, todos `test(...)` — nenhuma linha de `main.py` mudou, porque a implementação da 06 já cobria tudo e o valor estava em provar cada ramo. O RED foi demonstrado revertendo o comportamento observável (`action_baixo`, o `avisar` do `finally`, o `except ValueError, LinhaLonga`, o guard de `action_selecionar`) e restaurando, com diff líquido zero. O único RED genuíno de teste foi a mesa vazia/cheia: `desenhar_mesa` devolve **markup** (`[red]A♥[/red]`), não texto puro, e a asserção passou a comparar as linhas exatas. Cobertura de `main.py` subiu de 94% para 97% e o total de 97% para 98%.

**O que muda nas próximas sprints:** teste de função pura de tela precisa saber se ela devolve markup ou texto — `desenhar_carta`/`desenhar_mesa`/`desenhar_assentos` produzem markup do Textual, e só o `Static.render().plain` da tela remove as tags. Para tasks de "cobertura declarada", o RED se demonstra revertendo o comportamento observável, não inventando implementação.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| `meu_assento` ausente, `enviar` sem conexão e `main()` das fachadas | baixa | ramos defensivos/fachada; sem caminho de jogo quebrado |
| Idempotência de dois `Estado` iguais e `encerrado`/placar final | baixa | fora do escopo da 06; tela final é da 07 |
| `ConnectionResetError` em `Servidor._desconectar` (arrastado da 05) | baixa | só o fechamento abrupto do cliente dispara |

**Evidências:** `pi-spec/pysueca-v1/execucao/06-cliente-tui/relatorio-verificacao.md`

---

## Sprint 07-polimento — Polimento — 2026-10-12

**Aprendizado:** a sprint foi quase toda de tela e prosa, e o custo real esteve em dois pontos. (1) Trocar a mensagem de erro mudou o comportamento que **quatro testes da 06** asseguravam (código cru no `#aviso`): o RED deles apareceu ao rodar a suite depois do `MOTIVOS`, não ao escrever teste novo — os asserts antigos foram trocados em commits `test(...)` antes do `feat(...)`, mantendo a suite verde em todo commit de implementação e a lição de "não consertar depois". (2) O fallback do `frase_do_motivo` não pôde ser adiado para a task 2.11: o teste 2.1 do qa-plan exige comparar cada frase com a **genérica** (é o que faz um motivo novo do motor ficar vermelho), então o fallback entrou no primeiro GREEN e 2.11/2.12 viraram só o teste de cobertura. Medições desta sprint, não suposições: no Textual 8.2.8 `app.dark` não existe (o action troca `app.theme`, `textual-dark` ↔ `textual-light`); o `Footer.render()` devolve `Blank` no `run_test` e as teclas vivem nos filhos `FooterKey` (`key_display` renderizado: `←`, `→`, `⏎`, `^q`), que nem existem para `Binding(show=False)`; e `FooterKey` só aparece para ações distintas (bindings com a mesma action colapsam). `protocolo.py`, `motor.py` e `servidor.py` ficaram intactos: a tradução do motivo mora no `_traduzir` do cliente, na fronteira fio→tela da 06.

**O que muda nas próximas sprints:** antes de escrever o teste, listar os testes existentes que asseguram o comportamento que vai mudar e agendá-los como commits `test(...)` de RED antes do `feat(...)`. Quando um teste usa o fallback/valor default como oráculo, o fallback pertence ao primeiro GREEN — não criar task separada para ele. Para o rodapé do Textual, asseverar `app.query(FooterKey)` (`key_display`/`description`/`display`), nunca `Binding.show` nem `Footer.render()`. Um teste por edição de arquivo: dois testes na mesma região viram um hunk só e a separação em dois commits exige cirurgia de histórico.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste de tela do fim de jogo (`#mesa` com snapshot `encerrado`) em vez do render puro de `desenhar_mesa` | baixa | o render puro cobre a linha nova; o wiring do painel não muda |
| `encerrado` com `vencedor` nulo, `d` com o modal cima/baixo aberto e prioridade queda vs. erro no `#aviso` | baixa | ramos defensivos/de convivência de avisos; nenhum caminho de jogo quebrado |
| 5 linhas defensivas de `main.py`/`servidor.py` e `src/pysueca/__init__.py` fora da cobertura | baixa | arrastado das sprints 05/06; sem caminho de jogo quebrado |

**Evidências:** `pi-spec/pysueca-v1/execucao/07-polimento/relatorio-verificacao.md`

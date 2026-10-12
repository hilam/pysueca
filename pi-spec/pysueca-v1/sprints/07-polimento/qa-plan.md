# QA Plan — Sprint 07 — Polimento

> **Sprint:** `sprints/07-polimento/` — rastreia `sprints/07-polimento/specs/<capability>/spec.md`

## Capability: avisos

### Test: todo código de motivo do v1 vira frase de jogador
**Traces**: `sprints/07-polimento/specs/avisos/spec.md` → Requirement: Motivo de recusa em frase de jogador — CRITICAL
- **GIVEN** todos os códigos de motivo do v1: os três de `ErroJogada` (`fora_da_vez`, `carta_fora_da_mao`, `nao_seguiu_naipe`), os do servidor (`nome_em_uso`, `mesa_cheia`, `mesa_congelada`, `fora_de_hora`, `mesa_incompleta`, `nao_sentado`, `mensagem_invalida`) e os da forma do fio (`json_invalido`, `tipo_desconhecido`, `campo_extra`, `campo_faltando`, `campo_invalido`, `nome_invalido`)
- **WHEN** a função de tela que traduz o motivo roda (pura, sem `App`)
- **THEN** cada código devolve uma frase em português, sem `_`, diferente do código e não vazia — e o loop sobre `ErroJogada` faz um motivo novo do motor sem frase ficar vermelho (o cenário `todos os códigos do v1 têm frase própria`)

### Test: o nome em uso vira frase na tela
**Traces**: `sprints/07-polimento/specs/avisos/spec.md` → Requirement: Motivo de recusa em frase de jogador — CRITICAL
- **GIVEN** o cliente sentado com a tela de espera desenhada
- **WHEN** o servidor falso manda `erro` com motivo `nome_em_uso`
- **THEN** o `#aviso` mostra a frase de jogador e o app segue de pé; um `estado` seguinte limpa o aviso

### Test: EDGE - o JSON inválido vira frase
**Traces**: `sprints/07-polimento/specs/avisos/spec.md` → Requirement: Motivo de recusa em frase de jogador — EDGE
- **GIVEN** o cliente conectado
- **WHEN** o falso manda uma linha que não é JSON e o `desserializar` devolve `Erro("json_invalido")`
- **THEN** o `#aviso` mostra a frase de jogador e `json_invalido` não aparece na tela

### Test: EDGE - motivo desconhecido não vaza código nem derruba a tela
**Traces**: `sprints/07-polimento/specs/avisos/spec.md` → Requirement: Motivo de recusa em frase de jogador — EDGE
- **GIVEN** a função de tradução e um motivo que não existe no dicionário (`bug_novo`)
- **WHEN** a tradução roda
- **THEN** devolve a frase genérica, sem o código; e na tela, um `erro` com esse motivo deixa o app de pé

## Capability: fim-de-jogo

### Test: o fim do jogo aparece na mesa
**Traces**: `sprints/07-polimento/specs/fim-de-jogo/spec.md` → Requirement: Fim de jogo na tela — CRITICAL
- **GIVEN** o cliente sentado com quatro assentos ocupados
- **WHEN** o snapshot traz `encerrado` verdadeiro, `partidas == [4, 2]` e `vencedor == 0`
- **THEN** o `#mesa` mostra o fim do jogo, a dupla vencedora e o placar final `4 x 2`

### Test: a mesa encerrada não anuncia vez
**Traces**: `sprints/07-polimento/specs/fim-de-jogo/spec.md` → Requirement: Fim de jogo na tela — CRITICAL
- **GIVEN** o cliente conectado
- **WHEN** o snapshot traz `encerrado` verdadeiro com `vez == 0` e o assento do jogador é o 0
- **THEN** o `#aviso` não mostra `Sua vez`

### Test: a mesa encerrada não manda jogar
**Traces**: `sprints/07-polimento/specs/fim-de-jogo/spec.md` → Requirement: Fim de jogo na tela — CRITICAL
- **GIVEN** o cliente conectado com o snapshot de mesa encerrada e a mão ainda cheia
- **WHEN** o jogador aperta `Enter`
- **THEN** o falso não recebe `jogar` nenhum e nenhum motivo de recusa aparece no `#aviso`

### Test: EDGE - o nome ausente cai para a dupla
**Traces**: `sprints/07-polimento/specs/fim-de-jogo/spec.md` → Requirement: Fim de jogo na tela — EDGE
- **GIVEN** o cliente conectado com o snapshot de `encerrado` verdadeiro, `vencedor == 1` e o assento 3 sem nome
- **WHEN** a mesa é desenhada
- **THEN** a linha de fim mostra `dupla 1–3`, sem nome vazio nem `None`

### Test: EDGE - o jogo em andamento segue mostrando o placar simples
**Traces**: `sprints/07-polimento/specs/fim-de-jogo/spec.md` → Requirement: Fim de jogo na tela — EDGE
- **GIVEN** o cliente conectado
- **WHEN** o snapshot traz `encerrado` falso com `partidas == [1, 2]`
- **THEN** a mesa mostra o placar `1 x 2` e nenhuma linha de fim de jogo

## Capability: atalhos

### Test: as teclas de jogo aparecem no rodapé
**Traces**: `sprints/07-polimento/specs/atalhos/spec.md` → Requirement: Teclas de jogo visíveis no rodapé — CRITICAL
- **GIVEN** a tela do cliente montada dentro de `App.run_test()`
- **WHEN** os widgets de tecla do `Footer` são lidos
- **THEN** `left`/`Anterior`, `right`/`Próxima` e `enter`/`Jogar` estão entre as teclas visíveis, junto de `Sair` e de `d`/`Tema`

### Test: d alterna o tema
**Traces**: `sprints/07-polimento/specs/atalhos/spec.md` → Requirement: Tema claro e escuro — CRITICAL
- **GIVEN** a tela montada e o tema corrente anotado
- **WHEN** o jogador aperta `d` e depois `d` de novo
- **THEN** o tema troca para o outro (`textual-dark` ↔ `textual-light`) e volta ao primeiro

### Test: EDGE - o tema não muda a cor do naipe
**Traces**: `sprints/07-polimento/specs/atalhos/spec.md` → Requirement: Tema claro e escuro — EDGE
- **GIVEN** o desenho puro da carta
- **WHEN** `desenhar_carta("7H")` e `desenhar_carta("AD")` rodam
- **THEN** o markup segue `[red]7♥[/red]` e `[red]A♦[/red]`, sem variável de tema (cobertura: o markup fixo vem da 06, task 3.2)

## Capability: cliente

### Test: congelado, a recusa do servidor vira frase de jogador
**Traces**: `sprints/07-polimento/specs/cliente/spec.md` → Requirement: Tela de queda — EDGE
- **GIVEN** o cliente na sua vez com um assento em `ausentes`
- **WHEN** o jogador aperta `Enter` e o servidor recusa com `mesa_congelada`
- **THEN** o `#aviso` mostra a frase de mesa congelada e `mesa_congelada` não aparece; a tecla não é bloqueada localmente

### Test: EDGE - o erro do servidor aparece como frase
**Traces**: `sprints/07-polimento/specs/cliente/spec.md` → Requirement: Conexão em worker de tela — EDGE
- **GIVEN** o cliente conectado, na sua vez, com o snapshot já desenhado
- **WHEN** o falso manda `erro` com motivo conhecido (`fora_de_hora`)
- **THEN** o `#aviso` mostra a frase e o código não aparece; a tela segue lendo o fio (cobertura: o ramo é o do teste `o nome em uso vira frase na tela`; não declarar RED independente) — é o assert de `tests/test_cliente.py:319-321` reescrito

## Casos Limite

- `encerrado` verdadeiro com `vencedor` nulo: guard defensivo de uma linha (impossível no servidor v1, que sempre preenche o campo); sem teste RED independente, lição das sprints 01–03.
- `mesa_congelada` recusado com o banner de queda na tela: as duas frases convivem no `#aviso` e dizem coisas diferentes (a ação recusada e o estado da mesa, decisão 9); o teste da mesa congelada não fixa a contagem de frases.
- `assentos` com `None` no meio no fim do jogo: a dupla vencedora nomeia os jogadores que existem e cai para `dupla 0–2`/`dupla 1–3` quando falta um nome (decisão 10).
- `d` apertado com o modal cima ou baixo aberto: quem tem foco é a tela modal; `d` não está entre as teclas dela, então nada acontece com a jogada.
- `Enter` com a mesa encerrada: o cliente não manda `jogar` (decisão 12); as demais teclas seguem ativas e o servidor segue dono de qualquer outra recusa.
- Motivo de erro conhecido mas nunca visto em jogo (`tipo_desconhecido`, `nao_sentado`): a frase existe porque o loop do teste percorre o dicionário inteiro; o que o jogador vê em jogo depende do servidor.
- Mensagem de aviso local (`Sem conexão: …`, `Conexão encerrada`): passa intacta pela tradução, que só age nos códigos de motivo.
- Fim do jogo com a conexão caindo em seguida: o aviso de queda continua com prioridade sobre o aviso de erro (ordem de `texto_aviso`, sem regressão).

## Pontos de Integração

- `protocolo.Erro` (`protocolo.py:41,124,202`) é o único produtor dos motivos do fio; a tradução do cliente não muda o codec — o servidor segue mandando código (`servidor.py:71-122`) e o motor, `ErroJogada.value` (`motor.py:13-18` via `protocolo.py:90-92`).
- `Estado.encerrado`/`Estado.vencedor` (`protocolo.py:47-64`) chegam de `Jogo.encerrado`/`Jogo.vencedor` (`motor.py:176-183`); a tela os desenha pela primeira vez nesta sprint — o servidor não muda para o fim aparecer.
- `Estado.partidas` alimenta o placar final; a soma das partidas é do motor (`motor.py:166-174`), nunca da tela.
- `avisar`/`texto_aviso` (`main.py:244-270`) continuam sendo o único caminho do `Erro` até a tela; a tradução entra antes do `aviso_erro` e o teste 06 do aviso que sobrevive até o próximo snapshot segue valendo.
- `Footer` (`main.py:130-137`) lê os `Binding`s da `SuecaApp`; tirar o `show=False` de um binding muda o rodapé e o teste de teclas — uma fonte de verdade só. O `d` do tema é o mesmo caminho.
- `action_jogar` (`main.py:200-202`) ganha `estado.encerrado` junto do guard de mão vazia; nenhuma regra de jogo muda de dono, o servidor segue recusando toda jogada inválida.
- O `README.md` (`README.md:56-81`) e o `--host`/`--porta` do servidor (`servidor.py:196-197`) precisam concordar; um erro no passo a passo de duas máquinas só aparece na leitura humana.

## Notas de Revisão

- **NÃO TESTÁVEL**: `specs/comando/spec.md` → Scenario: `o README traz o passo a passo entre duas máquinas` (e o `o README traz o roteiro de quatro terminais`) — são prosa; a leitura é manual (task de validação final), e nenhum teste de documentação é criado, como na 06. Os cenários seguem normativos na spec.
- **RED esperado verde (cobertura, não RED independente)**: `o erro do servidor aparece como frase` cai no mesmo ramo de `o nome em uso vira frase na tela`; `o tema não muda a cor do naipe` cobre o markup fixo da 06. Entram no mesmo ciclo do vizinho, com a implementação adjacente — a lição das sprints 01–03 é não declarar vermelho para o que já está coberto.
- **Quatro testes da 06 mudam de propósito** (`tests/test_cliente.py:319-321,477-481,490-493,551-553`): o assert do código cru vira assert da frase. A troca é parte do ciclo RED→GREEN do `MOTIVOS`, não um "conserto" posterior; a suite tem de estar verde no commit.
- **O que o grill fechou (Questões Abertas do `design.md`, 2026-10-12):** fallback genérico puro; frase de motivo orientada à ação (sem dedup do banner); dupla vencedora nomeada com fallback; `d` visível no rodapé; `Enter` silenciado com a mesa encerrada; `MOTIVOS` com todos os códigos do v1. O comando que descobre o IP da mesa ficou delegado à implementação (decisão 14).
- **Asserção é sobre a tela e a tecla, não sobre o tipo**: os testes leem `Static.render().plain`, os `FooterKey` visíveis e `app.theme`; nenhum importa `protocolo` fora dos que já importavam.
- **Medido nesta sprint, não suposto**: `app.dark` não existe no Textual 8.2.8 (o action `toggle_dark` troca `app.theme`); `Footer.render()` devolve `Blank` no `run_test` e as teclas vivem nos filhos `FooterKey`. Os testes seguem o medido.
- **Determinismo**: nenhum `sleep`; os testes de tela usam o `ServidorFalso` e o `aguardar`/`pilot.pause()` da 06, e os testes de tradução são funções puras.

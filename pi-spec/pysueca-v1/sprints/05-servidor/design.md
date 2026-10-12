# Design — Sprint 05 — Servidor

> **Sprint:** `sprints/05-servidor/` — decisão do PLANO: o servidor é a única casca `asyncio`, valida intenções chamando `motor.py` e transmite snapshots (ADR 0001); queda de conexão congela a mesa e reserva o assento, sem timer (ADR 0005).
> **Depende de:** Sprint 04 — Protocolo (concluída)

## Contexto

As três camadas puras estão prontas e provadas: `Carta`/`Baralho` (01), `Vaza`/`Mao`/`Jogo` (02–03) e `protocolo.py` (04) — mensagens, codec de uma linha JSON em bytes, validação estrita com o teto de `TETO_LINHA` como único caso fatal, e o snapshot `estado(jogo, nomes, assento)` já montado por destinatário. O que não existe é o processo do meio: nada chama `asyncio.start_server`, nada traduz conexão em assento, nada avisa a mesa quando alguém cai. O ADR 0001 fixou o servidor dedicado e autoritativo e o ADR 0005 fixou a queda (avisa, congela, reserva, sem timer); o próprio `AGENTS.md` nomeia a 05 como a casca `asyncio`, e a 04 deixou de propósito sem dono: a fase da mesa, o campo de "congelada" (decisão 11 do design da 04) e os erros de assento e conexão (`nome_em_uso`, `mesa_cheia`, `nao_sentado`).

Esta sprint cria `src/pysueca/servidor.py` e `tests/test_servidor.py`, e acrescenta um campo ao `Estado` do protocolo.

## Objetivos / Não objetivos

**Objetivos:**
- `src/pysueca/servidor.py`: o `asyncio.start_server` com o teto do protocolo como limite de leitura, o handler por conexão, o mapa conexão→assento, os erros de assento/conexão, a pergunta cima ou baixo, a jogada pelo motor, o broadcast do snapshot por assento, a contagem da décima vaza e a queda que congela e reserva o assento — sem lock, porque não há corrida (decisão 3).
- `Estado.ausentes: list[int]` no `protocolo.py`, com serialização e validação estrita, para anunciar a queda sem tipo de mensagem novo (decisão 2).
- `tests/test_servidor.py` verde, com quatro clientes-robô concorrentes na série até o jogo encerrar (4 partidas, com a primeira mão contada no caminho), mais reconexão pelo nome, nome em uso, mesa cheia, jogada ilegal, mesa congelada e o teto fechando só aquela conexão.
- Reusar como estão `Jogo.preparar`/`jogar`/`encerrar_mao` (`motor.py:150,153,156`), `erro_de_jogada`, `estado`, `serializar`/`desserializar` e `jogada_legal` (nos robôs).

**Não objetivos:**
- Textual, widgets, tela de queda e seleção de carta — sprint 06.
- `python -m pysueca.servidor`, entrypoint e o `pyproject.toml:12` — sprint 06.
- Timer, jogador substituto, desistência e placar final na tela — ADR 0005 e sprint 07.
- Recomeçar o jogo depois das 4 partidas ("nova partida"/nova série): fora do v1 (Q3 do grill) — exige decidir quem dispara o recomeço e o que fazer com recusa parcial, o que é protocolo + tela; vira ADR próprio depois do v1.
- Autenticação, TLS, token de sessão e mais de uma mesa — fora do v1 (`docs/adr/0002`, `docs/adr/0005`).
- Reavaliar regra de jogo: o servidor não tem nenhum `if` de vez, posse ou naipe (fronteira das sprints 02/04).
- Um `asyncio.Lock`: o teste de concorrência não tem corrida para o lock resolver (decisão 3).

## Decisões

**1. `servidor.py` é a única casca `asyncio` do projeto.**
Critério: é a decisão do PLANO e o ADR 0001 — o processo do meio, e só ele, conhece rede e event loop; `carta.py`, `baralho.py`, `motor.py` e `protocolo.py` continuam síncronos e puros (invariante do `AGENTS.md`), então toda a regra é testável sem socket e o servidor é testável sem Textual. Alternativa rejeitada: embutir o `asyncio` no protocolo — acoplaria o formato de fio ao transporte, contra a decisão 1 da 04, e faria o teste de codec subir um servidor. Alternativa rejeitada: threads — o `Jogo` passaria a precisar de lock e o modelo dirigido a eventos do ADR 0002 se perderia.

**2. A queda viaja no `Estado`, como `ausentes: list[int]` — não como uma mensagem nova.**
Critério: o ADR 0002 diz que depois de cada evento o servidor reenvia o estado inteiro, e o ADR 0005 diz que a queda "avisa a mesa": o snapshot já é esse aviso, e a informação que falta (quem está sem conexão) é estado da mesa como qualquer outro. O ADR 0005 se lê exatamente assim, e a 04 já tinha deixado esse campo para a 05 (decisão 11 do design da 04: "a fase da mesa e o `congelada` ficam para a 05"). Alternativa rejeitada: um tipo `aviso`/`mesa` novo — mais um tipo no `_CAMPOS` do protocolo, mais um ramo no `match` do cliente (06) e mais um teste de ida-e-volta, para dizer um booleano. Alternativa rejeitada: `Estado.congelada: bool` — diz que a mesa parou, mas não **quem** caiu, e a tela de queda da 06 teria de adivinhar ou pedir mais um campo; `congelada` é `bool(ausentes)`, não precisa ser transmitido. Alternativa rejeitada: só um assento ausente por vez — duas quedas simultâneas não seriam representáveis.

**3. Sem lock: a mutação do `Jogo` acontece antes do primeiro `await` de cada intenção.**
Critério: o handler lê a linha (`await readline`), desserializa (síncrono), chama `Jogo.jogar`/`preparar`/`encerrar_mao` (síncrono) e só então faz `write`/`drain` (assíncrono); num event loop de thread única, entre voltar do `readline` e mutar o `Jogo` não existe ponto de suspensão, então duas jogadas nunca se intercalam na validação. Alternativa rejeitada: `asyncio.Lock` por mesa — não há corrida para ele resolver; só acrescentaria um `await` entre validar e mutar, e o teste de quatro clientes passaria igual. Alternativa rejeitada: uma fila de comandos consumida por uma única task — o gargalo serializa o que o event loop já serializa.

**4. O broadcast monta as quatro linhas antes de qualquer `write`, e envia só aos assentos ocupados.**
Critério: `estado(jogo, nomes, assento)` é síncrono; montar as quatro linhas de uma vez garante que todos vejam o **mesmo** estado (nenhum snapshot meio-atualizado entre um `drain` e outro) e que a ordem por conexão seja a ordem dos eventos. Assento nunca ocupado não tem `StreamWriter` e não recebe nada — a espera (`N de 4`) se lê em `assentos`. Alternativa rejeitada: montar o snapshot dentro do laço de envio — um `await` no meio deixaria o estado mudar entre as linhas. Alternativa rejeitada: mandar o mesmo dicionário a todos — vazaria a mão do destinatário para os outros; o snapshot é por assento (decisão 7 da 04).

**5. O limite do leitor é `TETO_LINHA`: `asyncio.start_server(..., limit=TETO_LINHA)`.**
Critério: o PLANO da 04 diz que o teto "vira a defesa de leitura do socket (05), onde o caso fatal de fato fecha a conexão". O `readline()` sem limite é o DoS de memória nomeado no ADR 0002/04; com o `limit`, o `StreamReader` recusa antes de o buffer crescer, e o servidor trata o estouro como o mesmo caso fatal — fecha só aquela conexão. `desserializar` continua sendo o contrato puro (o mesmo teto, contando o `\n`), e o servidor converte os dois no mesmo caminho. Alternativa rejeitada: ler sem limite e devolver `LinhaLonga` depois — quando a linha chega inteira, a memória já foi consumida, que é exatamente o ataque que o teto existe para cortar. Alternativa rejeitada: teto só no `desserializar` com limite de leitor folgado — dois números para a mesma defesa.

**6. Queda, EOF, reset e teto convergem para um `finally` único.**
Critério: as quatro causas terminam a conexão e a única diferença é o motivo; o handler fecha em `finally` chamando `desconectar(assento)`, que reserva o assento e transmite o snapshot. Um caminho só significa uma regra só (ADR 0005) e nenhuma causa esquecida — o teto do requisito 5 é literalmente a mesma queda. Alternativa rejeitada: tratar cada causa com um caminho próprio — três cópias do "reserva e avisa", e a que ninguém testou é a que vai ter bug. `desconectar(None)` (conexão que nunca sentou) não faz nada: não há nome a reservar.

**7. A mesa é o próprio `Servidor` — `nomes: list[str | None]`, `conexoes: list[StreamWriter | None]` e um `Jogo` (`Mesa` fica só no vocabulário do `CONTEXT.md`, não vira classe).**
Critério: `estado()` já recebe `nomes: list[str | None]` (decisão 7 da 04); o servidor é o único dono da ocupação, e os assentos são quatro posições fixas indexadas pelo protocolo. `ausentes` sai das conexões nulas, sem um quarto campo para manter em sincronia. Alternativa rejeitada: `Mesa` separada de `Servidor` — dois nomes para o mesmo objeto, e a `Mesa` precisaria dos `StreamWriter` do mesmo jeito, deixando o `Servidor` com o `start_server` e pouco mais. Alternativa rejeitada: dataclass `Assento(nome, conexao, reservado)` — três campos para quatro posições, sem invariante própria, e com um booleano `reservado` que pode mentir sobre a conexão.

**8. Os erros de assento e conexão são motivos estáveis no `Erro` existente.**
Critério: o `Erro` já carrega `motivo` como identificador estável (decisão 9 da 04), e a 04 deixou esses motivos explicitamente para a 05. Os do servidor: `nome_em_uso`, `mesa_cheia`, `nao_sentado`, `mesa_incompleta` (menos de quatro assentos), `mesa_congelada` (assento ausente), `fora_de_hora` (resposta cima ou baixo fora de hora — não é o respondente ou a mão já está preparada) e `mensagem_invalida` (intenção na direção errada — `estado`/`erro` vindos de cliente). Este último é fronteira de confiança: `desserializar` valida a forma, não a direção, então sem a guarda o bug de um cliente fica invisível. Os de jogada continuam vindo de `erro_de_jogada`. Alternativa rejeitada: enum `ErroMesa` no protocolo — tipos novos para strings estáveis que o cliente já sabe interpretar; o protocolo não ganha um segundo dono da regra de assento. Alternativa rejeitada: ignorar `estado`/`erro` em silêncio — nenhum código novo, mas um bug do cliente nunca aparece.

**9. A porta é parâmetro, e o teste usa a porta efêmera `0` com `getsockname()`.**
Critério: o harness do PLANO roda tudo em `localhost`, e o teste precisa de quatro conexões concorrentes sem colidir com nada nem deixar socket pendurado; `start_server(..., 0)` devolve um servidor já escutando, e a mesma `porta` serve para o passo a passo manual (`nc localhost <porta>`, risco global do PLANO). O servidor não escreve em `stdout` nem escolhe porta sozinho — quem decide é quem chama. Alternativa rejeitada: fixar 8765 no teste — flaky quando a porta está ocupada e proibido em CI concorrente.

**10. O servidor não revalida regra: `jogar` vai direto ao `Jogo.jogar` e o `ErroJogada` vira `Erro`.**
Critério: fecha a fronteira das sprints 02/04 — vez, posse e naipe têm um dono só, o `motor.py:117`; o servidor traduz o resultado e nada mais. Alternativa rejeitada: o servidor checar a vez antes de chamar o motor — duas verdades sobre a mesma regra, e a que o teste não cobrir é a que diverge.

**11. O fim da mão é a décima vaza, vista pelo servidor (`len(jogo.mao.vazas) == 10`).**
Critério: `Mao.vazas` já acumula as vazas fechadas (`motor.py:84`) e a mão do README tem dez; depois da décima, o servidor chama `encerrar_mao`, que soma o placar e abre a mão seguinte (ou encerra o jogo aos 4 partidas). A constante mora no servidor com o nome `VAZAS_POR_MAO`, porque é a casca que fecha o ciclo da mão. Alternativa rejeitada: `Mao.terminada` no motor — mudança no motor fora do escopo de uma sprint que é casca, para uma expressão de uma linha; se mais de um consumidor precisar do fim da mão, o motor ganha a propriedade com test próprio.

**12. A identidade é o nome, e só conexão viva bloqueia: o assento reservado é retomado por quem apresentar o nome.**
Critério: o ADR 0005 diz "o nome é a identidade" e recusa apenas o "nome já sentado **e ativo**"; quem caiu tem o assento reservado justamente para voltar — com o mesmo nome e um snapshot. Alternativa rejeitada: token de sessão — seria autenticação, explicitamente fora do v1 (ADR 0002/0005) e não prevista no protocolo (04). Risco aceito e registrado abaixo: qualquer um que saiba o nome retoma o assento, o que é aceitável em `localhost` e rede local (risco global do PLANO).

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| A mesa congelada vira ponto morto no teste (o risco nomeado no PLANO) | toda espera fica em `asyncio.wait_for` com timeout curto; `queda congela a mesa e avisa os outros três` assere explicitamente que o snapshot com `ausentes` chegou aos três, em vez de esperar o jogo andar |
| Quatro clientes concorrentes corrompem o estado | mutação síncrona antes do primeiro `await` (decisão 3) e as quatro linhas montadas antes dos `write` (decisão 4); o teste dos quatro robôs é a prova de carga |
| Um cliente que morre no meio de um `drain` derruba o servidor | o `write`/`drain` do broadcast é por conexão e a falha de uma não interrompe as outras; o `finally` do handler da conexão morta é quem reserva o assento (decisão 6) |
| O leitor fechar uma conexão legítima no limite | o limite é o mesmo `TETO_LINHA` da 04, e o EDGE `linha no limite é aceita` da 04 prova a fronteira fechada; o maior snapshot legítimo (10 cartas + 4 assentos + placar) fica abaixo de 1 KB |
| O teste ficar lento ou flaky | porta efêmera (decisão 9), `random.Random(seed)` injetado e robôs dirigidos a evento — a série inteira até as 4 partidas roda sem `sleep` e sem `timeout` real esperado |
| Um campo novo no `Estado` quebrar a 04 | `ausentes` entra com default `[]`, então os construtores existentes seguem válidos, e a serialização sempre o emite; o ida-e-volta da 04 passa a cobrir o campo |
| Vazamento de mão alheia no broadcast | o snapshot continua sendo montado assento a assento por `estado(jogo, nomes, assento)` (decisão 7 da 04); o broadcast nunca replica o mesmo payload (decisão 4) |
| A queda de quem nunca sentou "reservar" um assento inexistente | `desconectar(None)` é no-op (decisão 6); o teste `não sentado é recusado` cobre a conexão anônima |
| Depois do jogo encerrado (4 partidas) um `jogar` volta com motivo impreciso do motor | aceito: o jogo acabado tem as mãos vazias, então a jogada é recusada de todo jeito pelo motor; a mesa fica de pé com `encerrado`/`vencedor` no snapshot, sem reinício (Q2/Q3 do grill), e um motivo `mesa_encerrada` só entra se a tela (07) precisar dele |

## Plano de Migração

N/A — código aditivo (`src/pysueca/servidor.py`, `tests/test_servidor.py`) mais um campo com default em `Estado`. Nenhuma API existente muda; `carta.py`, `baralho.py`, `motor.py` e as funções do `protocolo.py` ficam intactas. Rollback: apagar os dois arquivos novos e reverter o campo `ausentes`. Nenhuma dependência nova (`docs/adr/0004`).

## Questões Abertas

Nenhuma — as pendências fecharam no grill:

- **`ausentes` (lista) ou `congelada` (booleano)?** Lista (decisão 2): a tela de queda (06) precisa de quem caiu, `congelada` é derivável e duas quedas simultâneas são representáveis.
- **Fim do jogo: reinício?** Não no v1 (Q3): a mesa fica de pé com `encerrado`/`vencedor`, sem motivo `mesa_encerrada` e sem recomeço; uma nova série vira ADR próprio depois do v1.
- **Quantos motivos de erro de assento?** Seis, mais `mensagem_invalida` (decisão 8): cada um é um estado de tela distinto, e `mesa_congelada` e `mesa_incompleta` não podem se confundir, assim como `fora_de_hora` não pode se passar por `mesa_incompleta` com a mesa cheia.
- **O teste dos quatro robôs assere o placar exato?** Não: invariantes (120 pontos na mão, partidas coerentes com o `Resultado`, quatro mãos vazias) com `random.Random(seed)` só para reproduzir a falha.
- **Rotação de mão coberta na 05?** Sim, de graça: os robôs jogam a série inteira até as 4 partidas, então a rotação do respondente passa por várias mãos.
- **Fim da mão: constante no servidor ou `Mao.terminada`?** `VAZAS_POR_MAO = 10` no `servidor.py` (decisão 11): o motor fica intocado e só ganha a propriedade se um segundo consumidor precisar.
- **`Mesa` e `Servidor` são classes distintas?** Não: uma classe só, `Servidor` (decisão 7); `Mesa` fica no `CONTEXT.md`.
- **Cliente manda `estado`/`erro`?** Recusa com `mensagem_invalida` (decisão 8): fronteira de confiança, `desserializar` não valida direção.

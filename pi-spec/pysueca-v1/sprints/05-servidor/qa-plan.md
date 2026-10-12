# QA Plan — Sprint 05 — Servidor

> **Sprint:** `sprints/05-servidor/` — rastreia `sprints/05-servidor/specs/<capability>/spec.md`

## Capability: servidor

### Test: entrar senta no primeiro assento livre
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Mesa autoritativa por assentos — CRITICAL
- **GIVEN** o servidor escutando em `127.0.0.1` na porta efêmera
- **WHEN** uma conexão manda `entrar` com o nome `"Ana"`
- **THEN** o snapshot devolvido traz `assentos[0] == "Ana"` e `mao` com dez cartas (a mão é preparada só depois, então `mao` vem vazia e `contagens` zeradas até o `responder`)

### Test: EDGE - nome já sentado e ativo é recusado
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Mesa autoritativa por assentos — EDGE
- **GIVEN** quatro robôs sentados, um deles com o nome `"Ana"`
- **WHEN** uma quinta conexão manda `entrar` com o nome `"Ana"`
- **THEN** ela recebe `erro` com motivo `nome_em_uso`, e os quatro assentos seguem como estavam

### Test: EDGE - mesa cheia recusa o quinto
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Mesa autoritativa por assentos — EDGE
- **GIVEN** os quatro assentos ocupados com nomes distintos
- **WHEN** uma quinta conexão manda `entrar` com um nome novo
- **THEN** ela recebe `erro` com motivo `mesa_cheia`, e a mesa não muda

### Test: EDGE - não sentado é recusado
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Mesa autoritativa por assentos — EDGE
- **GIVEN** uma conexão que nunca mandou `entrar`
- **WHEN** ela manda `jogar` e `responder`
- **THEN** recebe `erro` com motivo `nao_sentado` nas duas, e o servidor segue de pé

### Test: quatro assentos abrem a pergunta cima ou baixo
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Início da mão pelo respondente — CRITICAL
- **GIVEN** três robôs sentados e a mão ainda não preparada
- **WHEN** o quarto robô senta
- **THEN** os quatro recebem o snapshot com `respondente == (embaralhador + 1) % 4` (o parceiro do dador) e `trunfo is None`

### Test: responder prepara a mão e distribui dez cartas
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Início da mão pelo respondente — CRITICAL
- **GIVEN** os quatro robôs sentados e o `respondente` conhecido
- **WHEN** o assento respondente manda `responder` com `cima`
- **THEN** o snapshot transmitido a cada assento traz dez cartas na própria mão, `contagens == [10, 10, 10, 10]`, `trunfo` preenchido e `vez == embaralhador`

### Test: EDGE - responder fora de hora é recusado
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Início da mão pelo respondente — EDGE
- **GIVEN** a mesa com menos de quatro assentos ocupados, e depois com a mão preparada
- **WHEN** um assento manda `responder` nessas duas situações
- **THEN** recebe `erro` e o snapshot dos demais segue com `trunfo is None` na primeira e com a mesma mão na segunda

### Test: jogada ilegal vira erro só para quem jogou
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Jogada validada pelo motor — CRITICAL
- **GIVEN** a mão preparada e a vez de um assento conhecido
- **WHEN** um assento fora da vez manda `jogar`
- **THEN** só ele recebe `erro` com motivo `fora_da_vez`, os outros três não recebem nada, e a vez continua no mesmo assento

### Test: jogada legal chega aos quatro
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Jogada validada pelo motor — CRITICAL
- **GIVEN** a mão preparada e a vez de um assento conhecido
- **WHEN** ele manda `jogar` com uma carta da própria mão
- **THEN** os quatro recebem o snapshot novo, com a vaza trazendo `(assento, carta)`, a própria mão com nove cartas e as contagens coerentes

### Test: a décima vaza conta a mão
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Jogada validada pelo motor — CRITICAL
- **GIVEN** quatro robôs jogando a mão com `random.Random(seed)`
- **WHEN** a décima vaza fecha
- **THEN** os pontos da mão somam 120, a dupla vencedora soma exatamente as partidas que o `Resultado` daquela pontuação vale (ou `[0, 0]` no empate de 60 a 60), as quatro mãos ficam vazias e a mesa abre a mão seguinte — a seed só faz a falha reproduzir, não congela o placar

### Test: EDGE - mão nova volta a perguntar cima ou baixo
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Jogada validada pelo motor — EDGE
- **GIVEN** a primeira mão contada e o jogo ainda não encerrado
- **WHEN** o servidor abre a mão seguinte
- **THEN** o snapshot volta a trazer `respondente` preenchido, agora `(embaralhador_novo + 1) % 4`, e `trunfo is None`

### Test: o jogo encerrado não abre mão nova
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Jogada validada pelo motor — CRITICAL
- **GIVEN** quatro robôs jogando a série com `random.Random(seed)`
- **WHEN** uma dupla chega a 4 partidas
- **THEN** o último snapshot transmitido traz `encerrado` verdadeiro e `vencedor` daquela dupla, nenhuma mão nova é distribuída e as quatro conexões continuam de pé

### Test: EDGE - mensagem de direção errada é recusada
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Mesa autoritativa por assentos — EDGE
- **GIVEN** uma conexão sentada
- **WHEN** ela manda um `estado` e um `erro` como se fossem intenção
- **THEN** recebe `erro` com motivo `mensagem_invalida` nas duas, e o snapshot da mesa não muda

### Test: queda congela a mesa e avisa os outros três
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Queda congela a mesa e reserva o assento — CRITICAL
- **GIVEN** a mão preparada com quatro robôs na mesa
- **WHEN** a conexão de um assento fecha
- **THEN** os três assentos restantes recebem, dentro do timeout curto, o snapshot com aquele assento em `ausentes` e o nome ainda em `assentos`

### Test: EDGE - mesa congelada recusa jogadas
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Queda congela a mesa e reserva o assento — EDGE
- **GIVEN** a mesa congelada por um assento ausente
- **WHEN** um assento conectado manda `jogar` e `responder`
- **THEN** recebe `erro` com motivo `mesa_congelada` e a mão continua no mesmo ponto

### Test: reconexão com o mesmo nome retoma o assento
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Queda congela a mesa e reserva o assento — CRITICAL
- **GIVEN** a mesa congelada pelo assento ausente do nome `"Ana"`
- **WHEN** uma conexão nova manda `entrar` com o nome `"Ana"`
- **THEN** ela ocupa o mesmo assento, recebe o snapshot com as dez cartas da própria mão, os outros três recebem o snapshot com `ausentes` vazio e a mesa descongela (a jogada volta a ser aceita)

### Test: linha acima do teto fecha aquela conexão
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Linha acima do teto fecha só aquela conexão — CRITICAL
- **GIVEN** um assento sentado e a mesa em andamento
- **WHEN** essa conexão manda uma linha com mais de `TETO_LINHA` bytes
- **THEN** o servidor fecha só aquela conexão, o assento entra em `ausentes` no snapshot dos demais, e nenhuma exceção escapa ao servidor

### Test: EDGE - os outros três seguem na mesa
**Traces**: `sprints/05-servidor/specs/servidor/spec.md` → Requirement: Linha acima do teto fecha só aquela conexão — EDGE
- **GIVEN** a conexão fechada pelo teto
- **WHEN** os três assentos restantes reconectam o ausente pelo nome
- **THEN** a mesa volta ao ponto anterior — mesmo `vez`, mesmas contagens — e continua aceitando jogadas

## Capability: protocolo

### Test: estado carrega os assentos ausentes
**Traces**: `sprints/05-servidor/specs/protocolo/spec.md` → Requirement: Snapshot por assento — CRITICAL
- **GIVEN** um snapshot com `ausentes == [2]` e outro com `ausentes == []`
- **WHEN** cada um é serializado e desserializado
- **THEN** volta o mesmo `Estado`, com a lista de ausentes preservada e o campo presente na linha JSON

### Test: EDGE - ausentes com tipo errado vira erro
**Traces**: `sprints/05-servidor/specs/protocolo/spec.md` → Requirement: Snapshot por assento — EDGE
- **GIVEN** a linha de um `estado` com `"ausentes": "todos"`
- **WHEN** `desserializar` a lê
- **THEN** devolve `erro` com motivo `campo_invalido` (a validação estrita da 04, aplicada ao campo novo)

## Casos Limite

- A conexão que nunca sentou e cai não reserva assento: `desconectar(None)` é no-op (a mesa não ganha um ausente fantasma).
- `ausentes` é lista, não booleano: duas quedas simultâneas têm de ser representáveis (`[1, 3]`).
- Assento nunca ocupado **não** entra em `ausentes` — a espera se lê em `assentos`, a queda só em quem já estava sentado.
- O teto é contado em bytes UTF-8 e a linha inclui o `\n`; o limite do leitor é o mesmo número, então o EDGE `linha no limite é aceita` da 04 continua valendo.
- Uma conexão anônima que estoura o teto é fechada sem mexer na mesa (nada a reservar).
- `responder` do assento certo com a mão já preparada é recusa, não uma segunda preparação (o trunfo não muda).
- Nome reservado (dono caído) aceita o nome de volta; nome de conexão viva não (`nome_em_uso`) — a diferença é a conexão, não o nome.
- O servidor não escreve em `stdout` nem escolhe porta: quem chama decide (`127.0.0.1:0` no teste).
- `desserializar` valida a forma, não a direção: `estado`/`erro` vindos de cliente são recusa (`mensagem_invalida`), não um caminho silencioso.
- A série até as 4 partidas é o teste do fim do jogo; não há `mesa_encerrada` nem reinício no v1 — a mesa fica de pé para o placar.

## Pontos de Integração

- `Jogo.preparar`/`jogar`/`encerrar_mao` (`motor.py:150,153,156`) são as três únicas portas de mutação da mão; o servidor não tem `if` de vez/posse/naipe (decisões 1 e 10).
- `erro_de_jogada` (04) traduz o `ErroJogada` (`motor.py:13`); os motivos de assento da 05 (`nome_em_uso`, `mesa_cheia`, `nao_sentado`, `mesa_congelada`) reusam o mesmo `Erro` sem tipo novo (decisão 8).
- `estado(jogo, nomes, assento)` (04) monta o snapshot; o servidor só acrescenta `ausentes` e entrega um snapshot por assento (decisões 2 e 4).
- `TETO_LINHA` (`protocolo.py:11`) é o `limit` do `asyncio.start_server` e o teto do `desserializar`; os dois convergem para o mesmo fechamento (decisão 5).
- `jogada_legal` (`motor.py:21`) e `Carta.de_texto`/`texto` (`carta.py:71,75`) são reusados pelos robôs do teste — nenhum segundo formato de carta nem segunda regra de legalidade.
- A TUI (06) consome `ausentes` para a tela de queda e a 07 usa `encerrado`/`vencedor` para o placar final; nenhuma das duas entra nesta sprint.

## Notas de Revisão

- **O harness é o próprio entregável:** o PLANO diz que este teste "substitui os quatro terminais" — os robôs são clientes de verdade (conectam, entram, respondem, jogam e reconectam), não chamadas diretas ao servidor; o teste dos quatro robôs é a prova de concorrência da decisão 3.
- **Sem `pytest-asyncio`:** os testes são funções síncronas que chamam `asyncio.run(cenario())` — stdlib pura, nenhuma dependência nova (`docs/adr/0004`); um plugin só para marcar testes que já sabem rodar sob `asyncio.run` seria dependência de conforto.
- **Timeout curto é asserção, não espera:** o risco nomeado no PLANO (mesa congelada como ponto morto) vira `asyncio.wait_for` com folga pequena sobre trabalho dirigido a evento; nada no teste espera o relógio andar.
- **O que o grill fechou (Questões Abertas do `design.md`):** `ausentes` como lista; fim do jogo sem motivo próprio e sem reinício no v1 (ADR futuro); cinco motivos de assento mais `mensagem_invalida`; asserção por invariante com seed, não placar congelado; série completa até as 4 partidas para cobrir `encerrado`/`vencedor`; `VAZAS_POR_MAO = 10` no servidor com o motor intocado; uma classe `Servidor` (não `Mesa` + `Servidor`).
- **Cobertura dos novos caminhos:** `mesa_cheia`, `nao_sentado`, `mesa_congelada`, `mensagem_invalida` e `campo_invalido` em `ausentes` ancoram decisões 2 e 8 — se falharem, a decisão do grill não chegou ao código.
- **Fim do jogo coberto na 05:** o teste da série leva os robôs até a quarta partida e assere `encerrado`/`vencedor` no fio, então a transmissão do fim do jogo deixa de ser dívida; a tela do placar final continua na 07.

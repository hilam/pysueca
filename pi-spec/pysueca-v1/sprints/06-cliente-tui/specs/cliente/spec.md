# Spec — Capability `cliente`

> **Sprint:** `sprints/06-cliente-tui/` — capability `cliente` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Conexão em worker de tela
O cliente SHALL abrir uma conexão TCP com o servidor e SHALL ler cada linha do fio em um worker `asyncio` do Textual, traduzindo a mensagem recebida em estado de tela. Nenhum widget SHALL conhecer `protocolo.py` nem o significado do fio: a tradução SHALL terminar antes de qualquer `Widget.update`. O cliente SHALL mandar `entrar` com o próprio nome ao conectar, e SHALL derivar o próprio assento do nome em `assentos`, sem campo novo no protocolo. Um `erro` do servidor, uma linha malformada ou o fim da conexão SHALL virar aviso de tela e MUST NOT derrubar o app.

#### Scenario: o cliente manda entrar com o nome
- **WHEN** o cliente conecta e o servidor aceita a conexão
- **THEN** a primeira mensagem no fio é `entrar` com o nome do jogador, e o cliente passa a ler as linhas do snapshot

#### Scenario: o cliente se reconhece pelo nome
- **WHEN** o snapshot traz o nome do jogador em `assentos`
- **THEN** o cliente trata aquele índice como o próprio assento, para vez, respondente e jogada

#### Scenario: erro do servidor aparece sem derrubar o app
- **WHEN** o servidor manda `erro` com um motivo
- **THEN** o cliente mostra o motivo na tela e segue lendo o fio

#### Scenario: mensagem inválida do fio não derruba o app
- **WHEN** o servidor manda uma linha que o `desserializar` recusa
- **THEN** o cliente mostra um aviso e continua de pé

#### Scenario: sem servidor o cliente avisa e segue
- **WHEN** a conexão falha na abertura ou o servidor fecha o fio
- **THEN** o cliente mostra um aviso de conexão e segue de pé, sem exceção no loop

### Requirement: Espera pela mesa completa
Enquanto o snapshot não trouxer o trunfo, o cliente SHALL mostrar quantos dos quatro assentos estão ocupados e os nomes de quem sentou, e MUST NOT oferecer jogada. A contagem SHALL vir dos nomes não nulos de `assentos`. O cliente SHALL mostrar, ao lado de cada nome, a contagem de cartas daquele assento (`contagens`).

#### Scenario: tela de espera mostra N de 4 assentos
- **WHEN** o snapshot traz dois nomes em `assentos` e o trunfo ainda não preparado
- **THEN** a tela mostra `2 de 4` e os dois nomes, com os dois assentos vagos visíveis

#### Scenario: os assentos mostram a contagem de cartas
- **WHEN** o snapshot traz `contagens == [10, 9, 10, 10]`
- **THEN** a tela mostra, ao lado do nome de cada assento, quantas cartas aquele jogador tem

### Requirement: Mão de cartas em texto
O cliente SHALL desenhar a própria mão como cartas em texto (`A♥`, `7♠`) em uma única linha, com copas e ouros em vermelho, e SHALL destacar a carta selecionada. Os pontos de naipe SHALL ser os quatro símbolos do ADR 0004, sem uso dos PNGs de `docs/imagens/`.

#### Scenario: a mão desenha as cartas com o naipe colorido
- **WHEN** a mão do snapshot traz `"7H"` e `"7C"`
- **THEN** a carta de copas aparece vermelha com `♥` e a de paus aparece com `♣` sem cor de naipe

#### Scenario: a mesa mostra trunfo, vaza e placar
- **WHEN** o snapshot traz `carta_trunfo == "AH"`, uma vaza em andamento e o placar
- **THEN** a tela mostra a carta do trunfo (`A♥`), cada carta da vaza junto do seu assento e as partidas por dupla

### Requirement: Jogada pela seleção
`←` e `→` SHALL mover a seleção dentro da própria mão, sem passar dos limites, e `Enter` SHALL enviar `jogar` com a carta selecionada. O cliente SHALL enviar `jogar` sem revalidar vez, posse ou naipe — a regra tem um dono só, o servidor. Quando a mão muda, a seleção SHALL voltar à primeira carta, para nenhuma jogada apontar para uma carta que não está mais na mão.

#### Scenario: ←/→ movem a seleção e Enter joga a carta
- **WHEN** o cliente está na sua vez e a mão tem cartas
- **THEN** `→` avança o destaque, `←` recua, e `Enter` manda `jogar` com a carta destacada

#### Scenario: a seleção não passa dos limites da mão
- **WHEN** a seleção está na primeira ou na última carta e o jogador aperta `←` ou `→`
- **THEN** a seleção fica onde está, sem índice negativo nem fora da mão

#### Scenario: fora da vez o servidor decide
- **WHEN** `Enter` é apertado quando a vez não é do jogador
- **THEN** o cliente manda `jogar` mesmo assim e mostra o motivo do `erro` que o servidor devolver, sem checar a vez sozinho

#### Scenario: a seleção volta à primeira carta com a mão nova
- **WHEN** o snapshot traz uma mão nova
- **THEN** o destaque volta à primeira carta da mão

#### Scenario: com a mão vazia nada é jogado
- **WHEN** `Enter` é apertado com a mão do snapshot vazia
- **THEN** o cliente não manda `jogar`

### Requirement: Pergunta cima ou baixo
Quando o snapshot apontar `respondente` no assento do jogador e o trunfo ainda não estiver preparado, o cliente SHALL abrir um diálogo com as duas respostas. `c` SHALL enviar `responder` com `cima` verdadeiro e `b` SHALL enviar `responder` com `cima` falso. O diálogo SHALL fechar quando o trunfo for preparado, e MUST NOT abrir para um assento que não é o respondente.

#### Scenario: cima ou baixo abre na tela do respondente
- **WHEN** o snapshot traz o assento do jogador como `respondente` e o trunfo ainda não preparado
- **THEN** o diálogo aparece perguntando cima ou baixo

#### Scenario: cima ou baixo responde
- **WHEN** o diálogo está aberto e o jogador aperta `c` ou `b`
- **THEN** o cliente manda `responder` com o valor da tecla e fecha o diálogo

#### Scenario: quem não é o respondente não vê o diálogo
- **WHEN** o snapshot traz `respondente` em outro assento
- **THEN** o diálogo não aparece

### Requirement: Tela de queda
Quando o snapshot trouxer assento ausente em `ausentes`, o cliente SHALL mostrar quais assentos caíram e que a mesa está congelada; quando `ausentes` esvaziar, o aviso SHALL sumir. O cliente MUST NOT bloquear a jogada por causa do congelamento: a recusa é do servidor (`mesa_congelada`).

#### Scenario: a queda aparece na tela
- **WHEN** o snapshot traz um assento em `ausentes`
- **THEN** a tela mostra o nome daquele assento como caído e que a mesa espera

#### Scenario: reconexão limpa a tela de queda
- **WHEN** o snapshot seguinte traz `ausentes` vazio
- **THEN** o aviso de queda some da tela

#### Scenario: congelado o cliente ainda manda e o servidor recusa
- **WHEN** o jogador aperta `Enter` com um assento em `ausentes`
- **THEN** o cliente manda `jogar` mesmo assim e mostra o motivo `mesa_congelada` que o servidor devolver, sem bloquear a tecla localmente

## MODIFIED Requirements

(nenhum)

## REMOVED Requirements

(nenhum)

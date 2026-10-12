# Spec — Capability `servidor`

> **Sprint:** `sprints/05-servidor/` — capability `servidor` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Mesa autoritativa por assentos
O servidor SHALL ser o único dono do `Jogo` e dos quatro assentos, e SHALL ligar cada conexão a no máximo um assento. `entrar` SHALL sentar o nome no primeiro assento livre e SHALL responder com o snapshot daquele assento. O nome de um assento com conexão viva SHALL ser recusado com `erro nome_em_uso`, e `entrar` sem assento livre SHALL ser recusado com `erro mesa_cheia`; nenhuma dessas recusas MUST derrubar a mesa. `jogar` ou `responder` de uma conexão que ainda não sentou SHALL ser recusado com `erro nao_sentado`. Uma mensagem que o protocolo destina ao servidor (`estado` ou `erro`) SHALL ser recusada com `erro mensagem_invalida`, porque o cliente não manda estado.

#### Scenario: entrar senta no primeiro assento livre
- **WHEN** uma conexão manda `entrar` com um nome novo e há assento livre
- **THEN** o servidor a senta no primeiro assento livre, guarda o nome e devolve o snapshot daquele assento

#### Scenario: nome já sentado e ativo é recusado
- **WHEN** uma conexão manda `entrar` com o nome de um assento cuja conexão está viva
- **THEN** o servidor devolve `erro` com motivo `nome_em_uso` e a mesa não muda

#### Scenario: mesa cheia recusa o quinto
- **WHEN** as quatro posições estão ocupadas e uma conexão manda `entrar` com um nome novo
- **THEN** o servidor devolve `erro` com motivo `mesa_cheia` e a mesa não muda

#### Scenario: não sentado é recusado
- **WHEN** uma conexão que ainda não sentou manda `jogar` ou `responder`
- **THEN** o servidor devolve `erro` com motivo `nao_sentado` e a mão não muda

#### Scenario: mensagem de direção errada é recusada
- **WHEN** uma conexão sentada manda `estado` ou `erro` como se fosse intenção
- **THEN** o servidor devolve `erro` com motivo `mensagem_invalida` e a mesa não muda

### Requirement: Início da mão pelo respondente
Depois de cada assento ocupado, o servidor SHALL transmitir o snapshot a todos os assentos ocupados. Com os quatro assentos ocupados e a mão ainda não preparada, o snapshot SHALL apontar como `respondente` o parceiro do dador, e `responder` desse assento SHALL preparar a mão com `cima`/`baixo` e transmitir o snapshot das dez cartas. `responder` de um assento que não é o respondente, com a mesa incompleta ou com a mão já preparada, SHALL ser recusado com `erro mesa_incompleta` (menos de quatro assentos) ou `erro fora_de_hora` (não é o respondente ou a mão já preparada) e MUST NOT mudar a mão.

#### Scenario: quatro assentos abrem a pergunta cima ou baixo
- **WHEN** o quarto assento é ocupado
- **THEN** o snapshot transmitido aponta `respondente` no parceiro do dador, com o trunfo ainda não preparado

#### Scenario: responder prepara a mão e distribui dez cartas
- **WHEN** o assento respondente manda `responder` com `cima`
- **THEN** o servidor prepara a mão, cada assento recebe o snapshot com dez cartas na própria mão e `vez` no embaralhador

#### Scenario: responder fora de hora é recusado
- **WHEN** um assento manda `responder` sem ser o respondente, ou com a mesa incompleta, ou com a mão já preparada
- **THEN** o servidor devolve `erro mesa_incompleta` com a mesa incompleta e `erro fora_de_hora` nos outros dois casos, e a mão continua como estava

### Requirement: Jogada validada pelo motor
O servidor SHALL validar cada `jogar` chamando `Jogo.jogar` (`motor.py:153`), sem reavaliar vez, posse ou naipe. Um `ErroJogada` SHALL virar `erro` endereçado só à conexão que jogou, e a mesa SHALL seguir. Uma jogada legal SHALL ser transmitida a todos os assentos ocupados como snapshot novo. Quando a décima vaza fecha, o servidor SHALL contar a mão com `Jogo.encerrar_mao` (`motor.py:156`) e transmitir o placar; se o jogo não acabou, a mão seguinte SHALL abrir a pergunta cima ou baixo para o novo respondente. Ao somar a quarta partida, o servidor SHALL encerrar o jogo, transmitir o snapshot final com `encerrado` e `vencedor` e MUST NOT abrir mão nova; a mesa SHALL continuar de pé para o cliente ler o placar.

#### Scenario: jogada ilegal vira erro só para quem jogou
- **WHEN** um assento joga fora da vez, uma carta que não está na própria mão ou fora do naipe puxado
- **THEN** só aquela conexão recebe `erro` com o motivo do `ErroJogada`, e a mesa continua na mesma jogada

#### Scenario: jogada legal chega aos quatro
- **WHEN** o assento da vez joga uma carta legal
- **THEN** os quatro assentos ocupados recebem o snapshot novo, cada um com a própria mão e a contagem das outras

#### Scenario: a décima vaza conta a mão
- **WHEN** a décima vaza fecha
- **THEN** o servidor conta a mão e transmite o snapshot com `partidas` somado à dupla vencedora

#### Scenario: mão nova volta a perguntar cima ou baixo
- **WHEN** a mão foi contada e o jogo não acabou
- **THEN** o snapshot transmitido volta a apontar `respondente`, agora o parceiro do embaralhador da mão nova

#### Scenario: o jogo encerrado não abre mão nova
- **WHEN** a mão contada leva uma dupla a 4 partidas
- **THEN** o snapshot final traz `encerrado` verdadeiro e `vencedor` da dupla, e nenhuma mão nova é distribuída

### Requirement: Queda congela a mesa e reserva o assento
Quando uma conexão cai, o servidor SHALL manter o nome no assento, marcar o assento em `ausentes`, preservar o estado da mão e transmitir o snapshot a todos os assentos ocupados; a mesa SHALL ficar congelada e MUST NOT avançar sem os quatro. Enquanto houver assento ausente, `jogar` e `responder` SHALL ser recusados com `erro mesa_congelada`. `entrar` com o nome reservado SHALL devolver o jogador ao assento, tirar o assento de `ausentes` e transmitir o snapshot. Não há timer, desistência nem jogador substituto.

#### Scenario: queda congela a mesa e avisa os outros três
- **WHEN** a conexão de um assento cai no meio da mão
- **THEN** os três assentos restantes recebem o snapshot com aquele assento em `ausentes`, e a mão para

#### Scenario: mesa congelada recusa jogadas
- **WHEN** um assento conectado manda `jogar` ou `responder` enquanto há assento ausente
- **THEN** recebe `erro` com motivo `mesa_congelada` e a mão não muda

#### Scenario: reconexão com o mesmo nome retoma o assento
- **WHEN** uma conexão nova manda `entrar` com o nome reservado
- **THEN** ela ocupa aquele assento, que sai de `ausentes`, e recebe o snapshot da própria mão; a mesa descongela

### Requirement: Linha acima do teto fecha só aquela conexão
O servidor SHALL ler cada linha com o teto de bytes do protocolo (`TETO_LINHA`, `protocolo.py:11`) como limite do leitor. A linha acima do teto SHALL fechar aquela conexão — o único caso fatal do protocolo — como uma queda do assento, e MUST NOT derrubar o servidor nem a mesa.

#### Scenario: linha acima do teto fecha aquela conexão
- **WHEN** uma conexão manda uma linha com mais de `TETO_LINHA` bytes
- **THEN** o servidor fecha só aquela conexão, e o assento entra em `ausentes`

#### Scenario: os outros três seguem na mesa
- **WHEN** uma conexão é fechada pelo teto
- **THEN** o servidor continua servindo, e os outros três assentos seguem conectados à mesma mesa

## MODIFIED Requirements

(nenhum)

## REMOVED Requirements

(nenhum)

# Spec — Capability `protocolo`

> **Sprint:** `sprints/04-protocolo/` — capability `protocolo` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Mensagens de fio
O protocolo SHALL representar as mensagens do jogo como uma linha JSON em bytes UTF-8 terminada em `\n`, com os tipos `entrar`, `responder` e `jogar` (cliente → servidor) e `estado` e `erro` (servidor → cliente). Cada mensagem SHALL fazer ida-e-volta sem perda: desserializar o texto que `serializar` produziu SHALL reproduzir a mensagem original. A carta SHALL viajar no formato `"7H"` de `Carta.texto()`.

#### Scenario: entrar faz ida-e-volta
- **WHEN** uma mensagem `entrar` com um nome é serializada e desserializada
- **THEN** volta a mesma mensagem `entrar` com o mesmo nome

#### Scenario: responder faz ida-e-volta
- **WHEN** uma mensagem `responder` com `cima` verdadeiro ou falso é serializada e desserializada
- **THEN** volta a mesma mensagem com o mesmo valor de `cima`

#### Scenario: jogar faz ida-e-volta
- **WHEN** uma mensagem `jogar` com a carta `"7H"` é serializada e desserializada
- **THEN** volta a mesma `Carta(COPAS, SETE)`

#### Scenario: estado faz ida-e-volta
- **WHEN** um snapshot `estado` é serializado e desserializado
- **THEN** volta o mesmo snapshot, com os mesmos assentos, mãos, contagens, trunfo, vaza e placar

### Requirement: Validação estrita recuperável
O protocolo SHALL recusar com uma mensagem `erro` a linha que não é JSON, o JSON que não é objeto, o tipo desconhecido, a mensagem à qual falte campo obrigatório e a mensagem com campo que o protocolo não conhece; a recusa MUST NOT ser fatal, e a mesa SHALL seguir. O nome de `entrar` SHALL ser normalizado com `strip` antes de virar identidade e MUST ter de 1 a 20 caracteres; nome vazio depois do `strip` ou com mais de 20 caracteres SHALL virar `erro`.

#### Scenario: linha malformada vira erro
- **WHEN** uma linha que não é JSON é desserializada
- **THEN** devolve uma mensagem `erro` e não levanta exceção

#### Scenario: tipo desconhecido vira erro
- **WHEN** uma linha com um `tipo` que o protocolo não conhece é desserializada
- **THEN** devolve uma mensagem `erro` com o motivo do tipo desconhecido

#### Scenario: campo faltando vira erro
- **WHEN** uma linha `jogar` sem o campo `carta` é desserializada
- **THEN** devolve uma mensagem `erro` com o motivo do campo faltando

#### Scenario: campo extra vira erro
- **WHEN** uma linha `jogar` traz um campo que o protocolo não conhece
- **THEN** devolve uma mensagem `erro` com motivo `campo_extra`

#### Scenario: nome é normalizado
- **WHEN** um `entrar` traz um nome com espaços em volta
- **THEN** a identidade é o nome sem os espaços

#### Scenario: nome inválido vira erro
- **WHEN** um `entrar` traz um nome vazio ou com mais de 20 caracteres
- **THEN** devolve uma mensagem `erro` com o motivo do nome inválido

### Requirement: Teto de bytes por linha
Cada linha SHALL ter no máximo `TETO_LINHA` bytes em UTF-8, contando o terminador, e o teto SHALL ser aplicado na desserialização (leitura). A linha acima do teto SHALL ser o único caso fatal — o protocolo SHALL sinalizá-la para que o servidor feche a conexão —, porque ler a linha sem limite é DoS de memória; todo outro erro SHALL ser recuperável e virar `erro`.

#### Scenario: linha acima do teto é fatal
- **WHEN** uma linha com mais de `TETO_LINHA` bytes é desserializada
- **THEN** o protocolo sinaliza a violação de tamanho (erro fatal), distinta da recusa recuperável

#### Scenario: linha no limite é aceita
- **WHEN** uma linha tem exatamente `TETO_LINHA` bytes
- **THEN** é desserializada normalmente, sem violação de tamanho

#### Scenario: nenhum outro erro é fatal
- **WHEN** uma linha é malformada, tem tipo desconhecido ou campo faltando
- **THEN** a recusa é recuperável (mensagem `erro`), nunca a violação de tamanho

### Requirement: Snapshot por assento
O snapshot `estado` SHALL ser montado por destinatário: SHALL trazer a mão inteira do assento destinatário e apenas a **contagem** de cartas de cada assento — as cartas alheias MUST NOT aparecer em campo algum. O snapshot SHALL trazer ainda os assentos ocupados, o trunfo e a carta do trunfo, quem deve responder "cima ou baixo", a vaza em andamento, o placar de partidas e o fim do jogo.

#### Scenario: snapshot traz a própria mão
- **WHEN** um snapshot é montado para um assento
- **THEN** o campo da mão traz exatamente as cartas daquele assento

#### Scenario: snapshot traz só a contagem das outras mãos
- **WHEN** um snapshot é montado para um assento
- **THEN** as outras mãos aparecem somente como contagem de cartas, e nenhuma carta alheia aparece na linha

#### Scenario: snapshot reflete a mesa
- **WHEN** um snapshot é montado para uma mesa com trunfo virado, vaza em andamento e placar
- **THEN** traz o trunfo, a carta do trunfo, a vez, a vaza, o placar e o fim do jogo

#### Scenario: snapshot diz quem deve responder
- **WHEN** um snapshot é montado com a pergunta "cima ou baixo" pendente
- **THEN** `respondente` traz o assento que deve responder, e `None` quando não há pergunta

### Requirement: Erro de jogada formatado
O protocolo SHALL formatar o `ErroJogada` devolvido pelo motor (`motor.py:13`) como mensagem `erro`, cada motivo com o seu identificador estável (`fora_da_vez`, `carta_fora_da_mao`, `nao_seguiu_naipe`), sem reavaliar a regra da jogada.

#### Scenario: jogada fora da vez vira erro
- **WHEN** o motor recusa uma jogada com `ErroJogada.FORA_DA_VEZ`
- **THEN** o protocolo devolve um `erro` com o identificador `fora_da_vez`

#### Scenario: carta fora da mão vira erro
- **WHEN** o motor recusa uma jogada com `ErroJogada.CARTA_FORA_DA_MAO`
- **THEN** o protocolo devolve um `erro` com o identificador `carta_fora_da_mao`

#### Scenario: não seguir o naipe vira erro
- **WHEN** o motor recusa uma jogada com `ErroJogada.NAO_SEGUIU_NAIPE`
- **THEN** o protocolo devolve um `erro` com o identificador `nao_seguiu_naipe`

## MODIFIED Requirements

(nenhum — não há spec anterior desta capability nem requisito existente alterado)

## REMOVED Requirements

(nenhum)

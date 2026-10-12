# Spec — Capability `cliente`

> **Sprint:** `sprints/07-polimento/` — capability `cliente` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> Requisitos copiados de `sprints/06-cliente-tui/specs/cliente/spec.md` e editados; os demais requisitos da 06 seguem valendo sem mudança.

## MODIFIED Requirements

### Requirement: Conexão em worker de tela
O cliente SHALL abrir uma conexão TCP com o servidor e SHALL ler cada linha do fio em um worker `asyncio` do Textual, traduzindo a mensagem recebida em estado de tela. Nenhum widget SHALL conhecer `protocolo.py` nem o significado do fio: a tradução SHALL terminar antes de qualquer `Widget.update`. O cliente SHALL mandar `entrar` com o próprio nome ao conectar, e SHALL derivar o próprio assento do nome em `assentos`, sem campo novo no protocolo. Um `erro` do servidor, uma linha malformada ou o fim da conexão SHALL virar aviso de tela em linguagem de jogador, e MUST NOT derrubar o app.

#### Scenario: o cliente manda entrar com o nome
- **WHEN** o cliente conecta e o servidor aceita a conexão
- **THEN** a primeira mensagem no fio é `entrar` com o nome do jogador, e o cliente passa a ler as linhas do snapshot

#### Scenario: o cliente se reconhece pelo nome
- **WHEN** o snapshot traz o nome do jogador em `assentos`
- **THEN** o cliente trata aquele índice como o próprio assento, para vez, respondente e jogada

#### Scenario: erro do servidor aparece sem derrubar o app
- **WHEN** o servidor manda `erro` com um motivo
- **THEN** o cliente mostra a frase de jogador daquele motivo na tela e segue lendo o fio, sem o código do protocolo

#### Scenario: mensagem inválida do fio não derruba o app
- **WHEN** o servidor manda uma linha que o `desserializar` recusa
- **THEN** o cliente mostra um aviso de jogador e continua de pé

#### Scenario: sem servidor o cliente avisa e segue
- **WHEN** a conexão falha na abertura ou o servidor fecha o fio
- **THEN** o cliente mostra um aviso de conexão e segue de pé, sem exceção no loop

### Requirement: Tela de queda
Quando o snapshot trouxer assento ausente em `ausentes`, o cliente SHALL mostrar quais assentos caíram e que a mesa está congelada; quando `ausentes` esvaziar, o aviso SHALL sumir. O cliente MUST NOT bloquear a jogada por causa do congelamento: a recusa é do servidor (`mesa_congelada`). A recusa do servidor SHALL aparecer na tela em linguagem de jogador, como qualquer outro `erro`.

#### Scenario: a queda aparece na tela
- **WHEN** o snapshot traz um assento em `ausentes`
- **THEN** a tela mostra o nome daquele assento como caído e que a mesa espera

#### Scenario: reconexão limpa a tela de queda
- **WHEN** o snapshot seguinte traz `ausentes` vazio
- **THEN** o aviso de queda some da tela

#### Scenario: congelado o cliente ainda manda e o servidor recusa
- **WHEN** o jogador aperta `Enter` com um assento em `ausentes`
- **THEN** o cliente manda `jogar` mesmo assim e mostra na tela a frase de jogador da recusa — a frase da ação recusada, não a do estado da mesa —, sem bloquear a tecla localmente e sem o código `mesa_congelada`

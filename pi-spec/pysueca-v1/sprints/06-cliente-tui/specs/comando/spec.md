# Spec — Capability `comando`

> **Sprint:** `sprints/06-cliente-tui/` — capability `comando` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Cliente na linha de comando
O comando `pysueca` SHALL subir o cliente Textual com o nome do jogador como argumento obrigatório e SHALL aceitar `--host` e `--porta`, com defaults `127.0.0.1` e `8765`. O parsing SHALL ser `argparse` da stdlib; um argumento desconhecido ou um nome faltando SHALL terminar o comando com código de erro, sem subir a tela.

#### Scenario: o cliente lê nome, host e porta
- **WHEN** `pysueca Ana --host 10.0.0.2 --porta 9000` é executado
- **THEN** o cliente é montado com nome `Ana`, host `10.0.0.2` e porta `9000`

#### Scenario: o cliente usa os defaults
- **WHEN** `pysueca Ana` é executado sem host nem porta
- **THEN** o cliente aponta para `127.0.0.1:8765`

#### Scenario: argumento desconhecido sai com erro
- **WHEN** o comando recebe uma opção que não existe
- **THEN** termina com código de erro e não conecta

### Requirement: Servidor na linha de comando
O comando `pysueca-servidor` SHALL subir o servidor autoritativo e SHALL aceitar `--host` e `--porta`, com defaults `127.0.0.1` e `8765`. O comando SHALL ser a única casca `asyncio` de entrada de processo do servidor, e MUST NOT ser importado pelo cliente.

#### Scenario: o servidor lê host e porta
- **WHEN** `pysueca-servidor --porta 9000` é executado
- **THEN** o servidor escuta em `127.0.0.1:9000`

#### Scenario: o servidor usa a porta default
- **WHEN** `pysueca-servidor` é executado sem argumentos
- **THEN** o servidor escuta em `127.0.0.1:8765`

### Requirement: Roteiro manual de quatro terminais
O `README.md` SHALL documentar o roteiro de quatro terminais — o comando do servidor e um cliente por assento — e SHALL dizer que a ordem dos assentos é a ordem de conexão, com as duplas 0–2 e 1–3.

#### Scenario: o README traz o roteiro de quatro terminais
- **WHEN** alguém lê a seção de desenvolvimento do `README.md`
- **THEN** encontra o comando do servidor, os quatro comandos de cliente e a relação entre ordem de conexão e duplas

## MODIFIED Requirements

(nenhum)

## REMOVED Requirements

(nenhum)

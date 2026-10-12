# Spec — Capability `comando`

> **Sprint:** `sprints/07-polimento/` — capability `comando` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> Requisito copiado de `sprints/06-cliente-tui/specs/comando/spec.md` e editado; `Cliente na linha de comando` e `Servidor na linha de comando` seguem valendo sem mudança.

## MODIFIED Requirements

### Requirement: Roteiro manual de quatro terminais
O `README.md` SHALL documentar o roteiro de quatro terminais — o comando do servidor e um cliente por assento — e SHALL dizer que a ordem dos assentos é a ordem de conexão, com as duplas 0–2 e 1–3. O `README.md` SHALL documentar também o passo a passo de jogar entre duas máquinas: o servidor com o bind explícito para aceitar conexões de fora (`--host`) e cada cliente apontando para o endereço da máquina da mesa, com o comando para descobrir esse endereço e o aviso de que o firewall pode bloquear a porta. Por fim SHALL declarar o que o v1 entrega — quatro jogadores, uma série até 4 partidas, uma mesa por servidor — e o que fica fora dele.

#### Scenario: o README traz o roteiro de quatro terminais
- **WHEN** alguém lê a seção de desenvolvimento do `README.md`
- **THEN** encontra o comando do servidor, os quatro comandos de cliente e a relação entre ordem de conexão e duplas

#### Scenario: o README traz o passo a passo entre duas máquinas
- **WHEN** alguém lê a seção de desenvolvimento do `README.md` procurando como jogar de duas máquinas
- **THEN** encontra o comando do servidor com o bind que aceita conexão de fora, o comando do cliente apontando para o endereço da máquina da mesa, o comando que descobre esse endereço e o aviso do firewall

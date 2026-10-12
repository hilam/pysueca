# Proposal — Sprint 05 — Servidor

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 05 — Servidor
> **Depende de:** Sprint 04 — Protocolo (concluída)

## Por que

O motor inteiro (`motor.py:141`) e o formato de fio (`protocolo.py:47`) existem e estão provados, mas nada escuta o socket: não há processo dono da mesa, então quatro pessoas ainda não conseguem jogar e a TUI (06) não tem a quem se conectar. O ADR 0001 fixa o modelo — servidor dedicado, autoritativo, única casca `asyncio` — e o ADR 0005 fixa a queda: avisar a mesa, congelar o jogo e reservar o assento, sem timer e sem bot. Nenhum dos dois tem dono no código. Esta sprint fecha o `servidor.py`, e a prova é o harness que substitui os quatro terminais: quatro clientes-robô em `asyncio` jogando uma mão inteira por TCP em `localhost`.

## O que muda

- **`src/pysueca/servidor.py`** (novo) — a única casca `asyncio`: `asyncio.start_server` com o teto de bytes do protocolo como limite de leitura, um handler por conexão, o mapa conexão→assento, o `Servidor` (que **é** a mesa: os quatro nomes, as quatro conexões e o `Jogo`), o assento na chegada e na reconexão, a pergunta "cima ou baixo" do respondente, a jogada validada pelo motor, o broadcast do snapshot por assento, a contagem da décima vaza, o fechamento da conexão acima do teto, a recusa de intenção na direção errada (`estado`/`erro` vindos de cliente) e a queda que congela e reserva.
- **`src/pysueca/protocolo.py`** (modificado) — `Estado.ausentes: list[int]`: os assentos reservados sem conexão. É por esse campo que a queda do ADR 0005 ("o servidor avisa a mesa") chega aos outros três, dentro do snapshot que o ADR 0002 já manda a cada evento.
- **`tests/test_servidor.py`** (novo) — clientes-robô em `asyncio` (jogam a carta legal sorteada) contra o servidor em `127.0.0.1` na porta efêmera `0`, cobrindo a ida-e-volta de assento, a série até o jogo encerrar (4 partidas, com a primeira mão contada no caminho), os erros de assento e de direção, a queda, a reconexão e o teto.
- **`tests/test_protocolo.py`** (modificado) — o cenário `estado faz ida-e-volta` passa a cobrir `ausentes`.
- **`AGENTS.md`** (modificado) — o mapa de arquivos ganha `servidor.py` e a invariante da casca `asyncio`.

Nenhum arquivo do motor muda: o servidor chama `Jogo.preparar`/`jogar`/`encerrar_mao` (`motor.py:150,153,156`) e traduz o `ErroJogada` (`motor.py:13`) com `erro_de_jogada`, sem reavaliar vez, posse ou naipe. Nenhuma dependência nova (`docs/adr/0004`).

## Capabilities

### New Capabilities
- `servidor`: a mesa autoritativa servida por TCP — assentos e reconexão, intenções validadas pelo motor, broadcast do snapshot por assento, contagem da mão e a queda que congela e reserva.

### Modified Capabilities
- `protocolo`: o requisito **Snapshot por assento** ganha `ausentes` (os assentos reservados sem conexão), para que a mesa anuncie a queda sem um tipo de mensagem novo.

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/servidor.py` | arquivo novo — a única casca `asyncio` do projeto |
| `src/pysueca/protocolo.py:47` | `Estado` ganha `ausentes: list[int]` (default `[]`, então o construtor antigo segue válido) |
| `src/pysueca/protocolo.py:66` | intocado; `estado()` continua montando o snapshot; o servidor é quem sabe dos assentos ausentes e passa a lista |
| `src/pysueca/protocolo.py:91,122,156,181` | `_para_dados`, `_CAMPOS["estado"]` e o ramo `estado` de `desserializar` passam a carregar/validar `ausentes` (campo obrigatório no fio, como os demais) |
| `src/pysueca/protocolo.py:11` | `TETO_LINHA` vira o `limit` do `asyncio.start_server` — a defesa de memória do leitor; `LinhaLonga` (04) segue sendo o contrato puro |
| `src/pysueca/motor.py:141` | intocado; consumido por `preparar`, `jogar`, `encerrar_mao`, `partidas`, `encerrado`, `vencedor` e `mao.vazas` |
| `src/pysueca/motor.py:117` | intocado; a checagem de regra continua só no motor — o servidor não repete nenhum `if` de vez/posse/naipe |
| `src/pysueca/motor.py:21` | intocado; `jogada_legal` é reusado pelos robôs do teste para escolher uma carta legal |
| `src/pysueca/protocolo.py:21` | intocado; `Carta.texto`/`de_texto` (`carta.py:71,75`) são o único formato de carta, também no robô |
| `tests/test_servidor.py` | arquivo novo |
| `tests/test_protocolo.py` | o ida-e-volta de `estado` ganha `ausentes`; nenhum teste existente muda de comportamento |
| `src/pysueca/main.py:52` | intocado; `uv run mypy src` continua vermelho por `App.dark` (pré-existente, sprint 06) |
| `pyproject.toml:12` | intocado; o entrypoint quebrado e o comando de subir o servidor são da sprint 06 |
| `AGENTS.md` | mapa de arquivos ganha `servidor.py`; entra a invariante de que só ele usa `asyncio`/rede |
| `docs/adr/` | sem ADR novo: 0001, 0002 e 0005 já decidem; o `design.md` liga cada decisão ao seu ADR |

Consumidor imediato: a TUI (06) se conecta, desserializa `estado`/`erro` e serializa as intenções; `ausentes` é o que desenha a tela de queda. A sprint 07 liga o placar final ao `encerrado`/`vencedor`.

## Não objetivos

- Tela, cartas coloridas, seleção de carta e teclado — sprint 06.
- Subir o servidor por linha de comando (`python -m`/entrypoint) e fechar o `pyproject.toml:12` — sprint 06, junto com a TUI.
- Autenticação, TLS, token de sessão e mais de uma mesa — fora do v1 (`docs/adr/0002`, `docs/adr/0005`).
- Timer, jogador substituto e desistência — rejeitados no ADR 0005; a mesa espera o dono do assento.
- Regra de jogo no servidor: vez, posse da carta e naipe continuam no `motor.py:117`; o servidor só formata o `ErroJogada` recebido.
- Placar final na tela e mensagens de erro traduzidas para o jogador — sprint 07.
- Recomeçar o jogo depois das 4 partidas ("nova partida"/nova série) — fora do v1: exige decidir quem dispara o recomeço (um jogador? consenso dos quatro?) e o que fazer com recusa parcial, o que é feature de protocolo e tela, não detalhe do servidor; vira ADR próprio depois do v1.

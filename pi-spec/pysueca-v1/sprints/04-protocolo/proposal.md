# Proposal — Sprint 04 — Protocolo

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 04 — Protocolo
> **Depende de:** Sprint 03 — Jogo e papéis (concluída)

## Por que

O motor inteiro existe (`Jogo` em `motor.py:141`), mas nada o atravessa: não há formato de fio nem validação, então o servidor (05) não tem como receber `entrar`/`responder`/`jogar` nem transmitir o estado, e a TUI (06) não tem o que desenhar. O ADR 0002 fixa o transporte — TCP cru, uma linha JSON por mensagem, snapshot completo a cada evento —, mas o formato da linha e as regras de recusa ainda não têm dono: sem teto de bytes, um `readline()` sem limite é DoS de memória, e sem validação um JSON torto derruba a mesa. Esta sprint fecha o `protocolo.py` puro, sem rede, para que a 05 só ligue o socket.

## O que muda

- **`src/pysueca/protocolo.py`** (novo) — as mensagens (`entrar`, `responder`, `jogar`, `estado`, `erro`), o codec de uma linha JSON em bytes UTF-8 (`serializar`/`desserializar`), o teto de bytes por linha, a validação estrita (linha malformada, tipo desconhecido, campo faltando, campo extra, nome) e o snapshot `estado` por assento (própria mão + contagem das outras + `respondente` da pergunta cima/baixo).
- **`tests/test_protocolo.py`** (novo) — ida-e-volta das mensagens, o mascaramento do snapshot, a recusa recuperável (vira `erro`) e o teto de bytes como único caso fatal. Sem `asyncio`, sem socket, sem Textual.

Nenhum arquivo do motor muda: `protocolo.py` reusa `Carta.texto`/`de_texto` (`carta.py:71,75`), o `ErroJogada` (`motor.py:13`) e lê o estado do `Jogo` (`motor.py:141`). Nenhuma dependência nova (`docs/adr/0004`).

## Capabilities

### New Capabilities
- `protocolo`: o formato de fio — as cinco mensagens, o codec de uma linha JSON, a validação estrita (recuperável vs. fatal) e o snapshot por assento.

### Modified Capabilities
- (nenhuma — `carta`, `baralho` e `motor` são apenas consumidos)

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/protocolo.py` | arquivo novo — único módulo da sprint |
| `src/pysueca/carta.py:71,75` | sem mudança; `serializar`/`desserializar` usam `Carta.texto()` e `Carta.de_texto()` no formato `"7H"` |
| `src/pysueca/motor.py:13` | sem mudança; `erro_de_jogada` formata os três `ErroJogada` (`motor.py:16-18`) |
| `src/pysueca/motor.py:141` | sem mudança; `estado()` lê `Jogo.mao.maos`/`vez`/`vaza`/`trunfo`/`carta_trunfo`/`embaralhador` e `Jogo.partidas`/`encerrado`/`vencedor` (`respondente` derivado do embaralhador) |
| `src/pysueca/motor.py:117` | intocado; a checagem de regra (vez, posse, naipe) continua só no motor |
| `tests/test_motor.py`, `tests/test_jogo.py` | sem mudança; o snapshot os consome como fixtures reais |
| `tests/test_protocolo.py` | arquivo novo |
| `src/pysueca/main.py:52` | intocado; `uv run mypy src` continua vermelho por `App.dark` (pré-existente, sprint 06) |
| `pyproject.toml:6-12` | sem mudança; nenhuma dependência nova (`docs/adr/0004`) e o entrypoint quebrado continua fora de escopo |

Consumidores futuros: o servidor (05) chama `desserializar` a cada linha, `serializar` a cada envio e `estado(jogo, nomes, assento)` a cada snapshot; a TUI (06) desserializa `estado`/`erro` e serializa as intenções. O teto de bytes vira a defesa de leitura do socket (05), onde o caso fatal de fato fecha a conexão.

## Não objetivos

- Rede, socket, `asyncio`, reconexão e congelamento da mesa — sprint 05. Aqui o protocolo só sinaliza a linha fatal; quem fecha a conexão é o servidor.
- Tela, cartas coloridas e seleção de carta — sprint 06.
- Checagem de regra no protocolo: vez, posse da carta e naipe continuam no `motor.py:117`; o protocolo só formata o `ErroJogada` recebido (decisão 3 da sprint 02).
- Erros de assento/conexão (`nome_em_uso`, `não sentado`, mesa congelada) — servidor (05).

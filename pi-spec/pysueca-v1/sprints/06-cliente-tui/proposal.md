# Proposal — Sprint 06 — Cliente TUI

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 06 — Cliente TUI
> **Depende de:** Sprint 05 — Servidor (concluída); o fatiamento do PLANO abre a 06 logo após a 04, contra um servidor falso

## Por que

O servidor joga sozinho. `tests/test_servidor.py` prova uma mão inteira por TCP com quatro clientes-robô, mas nenhum humano vê tela: `src/pysueca/main.py` é um esqueleto Textual de 57 linhas com `Header`/`Footer` vazios (`main.py:41`), um `mypy` vermelho pré-existente (`main.py:52`) e nenhuma linha de socket. O `pyproject.toml:12` aponta para um entrypoint que não existe (`pysueca:src.pysueca.main`), então nem o cliente nem o servidor sobem por linha de comando — o roteiro de 4 terminais do PLANO não tem como ser escrito. O ADR 0001 exige que só o servidor toque a rede de forma autoritativa; o ADR 0004 fixa cartas em texto com naipe colorido, porque a única dependência permitida é o Textual, que não tem widget de imagem. Esta sprint fecha o último processo do v1: um cliente que conecta, desenha o snapshot e manda intenções, e o texto que ensina quatro pessoas a sentar nos quatro terminais.

## O que muda

- **`src/pysueca/main.py`** (reescrito) — o cliente Textual: o `SuecaApp(host, porta, nome)` com um worker `asyncio` que lê o fio e **só traduz mensagem em método de tela** (nenhum widget conhece `protocolo.py`), o assento derivado do próprio nome em `assentos` (sem campo novo no protocolo), a tela de espera (`N de 4`), a contagem de cartas por assento (`contagens`) e a carta do trunfo na mesa (`carta_trunfo`), a mão em uma linha com o naipe colorido, a seleção com `←`/`→`/`Enter`, o diálogo modal "cima ou baixo" e o painel de queda/erro. A função `main(argv)` com `argparse` fecha o entrypoint. O esqueleto sai inteiro: `PATH_IMAGENS`/`NAIPES`/`CARTAS` e o binding `d`/`action_toggle_dark` — a 07 re-liga o dark/light.
- **`src/pysueca/servidor.py`** (modificado) — `main(argv)` com `argparse` e `asyncio.run`, para o servidor subir por linha de comando.
- **`pyproject.toml:12`** (corrigido) — `pysueca = "pysueca.main:main"` e o segundo script `pysueca-servidor = "pysueca.servidor:main"`.
- **`tests/test_cliente.py`** (novo) — `App.run_test()` contra um servidor falso roteirizado (`asyncio.start_server` que serializa `Estado` de teste e grava as intenções recebidas), cobrindo a ida-e-volta de `entrar`, a espera, a mão, a seleção, o diálogo, a queda, o erro e a linha de comando.
- **`README.md:56`** (modificado) — o roteiro manual de 4 terminais.
- **`AGENTS.md`** (modificado) — `main.py` deixa de ser "esqueleto" e vira "o cliente Textual", com a invariante de que nenhum widget conhece o protocolo.

Nenhuma linha do motor, do baralho, do protocolo ou do servidor (fora do `main()` novo) muda: o cliente importa `Mensagem`, `serializar` e `desserializar` (`protocolo.py:64,95,162`) e usa `Carta.de_texto` (`carta.py:72`) — nenhuma regra de jogo nem formato de carta paralelo. Nenhuma dependência nova (`docs/adr/0004`).

## Capabilities

### New Capabilities
- `cliente`: a tela Textual conectada — worker de fio, espera pela mesa, mão em texto colorido, seleção de carta, pergunta cima ou baixo, aviso de queda e erro.
- `comando`: os dois comandos de linha (`pysueca` e `pysueca-servidor`), seus defaults e o roteiro de 4 terminais no `README.md`.

### Modified Capabilities
(nenhuma — nenhum requisito das specs 01–05 muda de comportamento)

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/main.py:1-57` | reescrito: `SuecaApp(host, porta, nome)`, o worker de leitura, os painéis e as ações de tecla; `PATH_IMAGENS`/`NAIPES`/`CARTAS` (o material de imagem) e o binding `d`/`action_toggle_dark` saem com o esqueleto |
| `src/pysueca/main.py:52` | o `mypy` vermelho pré-existente (`Cannot determine type of "dark"`) some com a reescrita |
| `src/pysueca/main.py:55` | o `if __name__ == "__main__"` vira `def main(argv)` — o entrypoint do `pyproject.toml` |
| `src/pysueca/protocolo.py:47,64,95,162` | intocado; o cliente consome `Estado`/`Erro`, `serializar` e `desserializar` como os testes da 04 e da 05 já provam |
| `src/pysueca/protocolo.py:11` | intocado; o cliente fecha a conexão no mesmo teto, do lado dele (o `readline` do cliente também pode estourar) |
| `src/pysueca/carta.py:72` | intocado; `Carta.de_texto` é o único desserializador de carta também na tela |
| `src/pysueca/motor.py` | intocado; a tela não conhece vez, posse nem naipe — mostra o que o snapshot traz |
| `src/pysueca/servidor.py:189` | ganha `main(argv)` com `argparse` e `asyncio.run(iniciar(...))`; `Servidor` e o handler ficam intactos |
| `pyproject.toml:12` | `pysueca = "pysueca.main:main"`; novo `pysueca-servidor = "pysueca.servidor:main"` |
| `tests/test_cliente.py` | arquivo novo — `App.run_test()` sem `pytest-asyncio` (mesma convenção da 05: `asyncio.run(cenario())`) |
| `tests/test_servidor.py` | intocado; os helpers de cliente-robô da 05 não são reaproveitados — o teste da 06 dirige a tela, não o jogo |
| `README.md:56` | a seção de desenvolvimento ganha o roteiro de 4 terminais |
| `AGENTS.md` | o mapa de arquivos atualiza `main.py`; a invariante "motor puro e síncrono" ganha a face do cliente: só o worker toca o fio |
| `docs/adr/` | sem ADR novo: 0001 (só o servidor é autoritativo), 0002 (snapshot completo) e 0004 (Textual e cartas em texto) já decidem; o `design.md` liga cada decisão ao seu ADR |

Consumidor imediato: o roteiro do `README.md` e as pessoas que vão jogar nos quatro terminais. A sprint 07 polimenta o que aqui é funcional: mensagens de erro traduzidas, placar final, teclas no `Footer` e o passo a passo de jogar entre duas máquinas.

## Não objetivos

- Traduzir os motivos de `erro` para linguagem de jogador, placar final do jogo, teclas no `Footer` e o bind para duas máquinas — sprint 07.
- Recomeçar a série depois das 4 partidas — fora do v1 (Q3 do grill da 05); a tela só mostra o que o snapshot traz.
- Autenticação, TLS, token de sessão, uma segunda mesa e seleção de assento na mão — fora do v1 (`docs/adr/0002`, `docs/adr/0005`); o assento é a ordem de conexão.
- Modo imagem com os PNGs de `docs/imagens/` — ADR 0004: exigiria dependência nova; o material fica para depois do v1.
- Re-ligar o dark/light e as teclas no `Footer` — sprint 07; a 06 remove o `d`/`action_toggle_dark` do esqueleto.
- Uma biblioteca de UI de terceiros, tema próprio ou CSS extenso — ADR 0004 e o teto de `80x24` do PLANO.
- Robôs de teste reaproveitados como clientes de verdade (`tests/test_servidor.py`) — o teste da 06 usa um servidor falso, não o `Servidor`.
- Snapshot do cliente em `stdout`/log: o fio já é inspecionável com `nc localhost 8765` (risco global do PLANO).

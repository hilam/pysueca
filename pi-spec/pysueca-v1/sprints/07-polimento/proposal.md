# Proposal — Sprint 07 — Polimento

> **Sprint do PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md` → Sprint 07 — Polimento
> **Depende de:** Sprint 06 — Cliente TUI (concluída)

## Por que

A mesa funciona, mas fala em código. Quem perde uma jogada lê `nao_seguiu_naipe` no `#aviso` (`main.py:244-270`, alimentado pelo `Erro` do fio (`protocolo.py:41,202`)); quem ganha o jogo vê `Placar: 4 x 2` e nada mais (`main.py:67`) — `encerrado` e `vencedor` chegam no snapshot (`protocolo.py:47-64`) e a tela os ignora, chegando a anunciar "Sua vez" numa mesa já encerrada, porque `vez` continua preenchido (`main.py:262-266`). O `d` que alternava o tema saiu com o esqueleto na 06, e as teclas de jogo estão no `Footer` com `show=False` (`main.py:115-117`): o rodapé anuncia só `Sair`. Por fim, o `README.md` ensina quatro terminais na mesma máquina (`README.md:64-81`) e não diz o que o v1 entrega nem como o servidor aceita conexão de fora — sem `--host 0.0.0.0` o `127.0.0.1` default (`servidor.py:196-197`) recusa o amigo na outra máquina. Esta sprint entrega o que o PLANO chama de "jogável por pessoas que não escreveram o código": motivo de recusa em português de jogador, o fim do jogo na tela, as teclas visíveis, o tema de volta e o passo a passo de duas máquinas.

## O que muda

- **`src/pysueca/main.py`** (modificado) — um dicionário `MOTIVOS` (código de fio → frase de jogador) com **todos os motivos do v1**, aplicado em `avisar`, com fallback genérico para motivo novo; `desenhar_mesa` ganha o fim de jogo (`encerrado`/`vencedor`), nomeando a dupla quando os dois nomes existem, e `texto_aviso` para de anunciar a vez quando `encerrado`; `action_jogar` soma `encerrado` ao guard de mão vazia, para a tecla de jogar não mandar jogada com a mesa acabada; o `Binding("d", "toggle_dark", "Tema")` volta visível no rodapé, junto das três teclas de jogo (`show=False` → visível).
- **`tests/test_cliente.py`** (modificado) — os quatro testes que asseguram o código cru (`"fora_de_hora"` em `tests/test_cliente.py:319-321`, `"nome_em_uso"` em `477-481`, `"json_invalido"` em `490-493`, `"mesa_congelada"` em `551-553`) passam a assegurar a frase; novos testes para o fim de jogo, o tema `d` e as teclas no rodapé.
- **`README.md:64-81`** (modificado) — o roteiro de quatro terminais permanece e ganha a seção de duas máquinas (servidor com `--host 0.0.0.0`, clientes com `--host <ip-da-mesa>`, o aviso de firewall) e a lista do que o v1 entrega.
- **`AGENTS.md`** (modificado) — o mapa de `main.py` ganha o fim de jogo, o `MOTIVOS` e as teclas de tela.

Nenhuma linha do motor, do baralho, do protocolo ou do servidor muda: a tradução mora no cliente, porque é o cliente que fala com o humano (`docs/adr/0002` — o fio é snapshot, não conversa). Nenhuma dependência nova (`docs/adr/0004`); o tema é o `action_toggle_dark` do próprio Textual (`textual/app.py`), não um tema próprio.

## Capabilities

### New Capabilities
- `avisos`: os motivos de recusa do fio em frase de jogador, com fallback para motivo não previsto.
- `fim-de-jogo`: o placar final, a dupla vencedora e o silêncio da vez numa mesa encerrada.
- `atalhos`: o `d` de volta ao tema claro/escuro e as teclas de jogo visíveis no `Footer`.

### Modified Capabilities
- `cliente`: os cenários `erro do servidor aparece sem derrubar o app` e `congelado o cliente ainda manda e o servidor recusa` deixam de exigir o código do protocolo na tela e passam a exigir a frase de jogador.
- `comando`: o requisito `Roteiro manual de quatro terminais` passa a cobrir também o passo a passo entre duas máquinas e o que o v1 entrega.

## Impacto

| Área | Efeito |
|---|---|
| `src/pysueca/main.py:244-248` | `avisar` passa o motivo por `MOTIVOS` antes de guardar no `aviso_erro`; o texto do `#aviso` deixa de ser código de fio |
| `src/pysueca/main.py:249-270` | `texto_aviso` para de anunciar a vez com `encerrado`; a prioridade queda > erro > vez > conexão fica intacta |
| `src/pysueca/main.py:56-71` | `desenhar_mesa` acrescenta o fim de jogo quando `estado.encerrado`, com a dupla de `vencedor` nomeada (fallback `dupla 0–2`/`dupla 1–3`) e as partidas finais |
| `src/pysueca/main.py:200-202` | `action_jogar` soma `estado.encerrado` ao guard de mão vazia — mesmo tipo de guard derivado do snapshot |
| `src/pysueca/main.py:113-117` | `Binding("d", "toggle_dark", "Tema")` volta, visível, e as três teclas de jogo perdem `show=False` |
| `src/pysueca/main.py:38-53` | intocado; o vermelho de copas e ouros é markup fixo, não variável de tema |
| `src/pysueca/main.py:150-187` | intocado; o worker e a tradução de fio seguem a fronteira da 06 |
| `src/pysueca/protocolo.py:11,47-64,95,162,187` | intocado; `Erro`, `Estado.encerrado` e `Estado.vencedor` já chegam do fio — é só desenhar |
| `src/pysueca/servidor.py:189-197` | intocado; o `--host` do servidor já existe — o que faltava era o `README.md` ensinar a usá-lo |
| `src/pysueca/motor.py:13-18,176-183` | intocado; `Resultado` e `Jogo.vencedor` são a fonte do placar final |
| `tests/test_cliente.py:306-324,472-496,538-556` | quatro testes trocam o código cru pela frase; os demais ficam intactos |
| `tests/test_cliente.py` (novos) | fim de jogo no `#mesa`, ausência de "Sua vez" com `encerrado`, `d` trocando `app.theme`, teclas no `Footer` e o fallback de motivo |
| `README.md:64-81` | a seção de desenvolvimento ganha o v1 pronto e o passo a passo de duas máquinas |
| `AGENTS.md` | o mapa de `main.py` cita o `MOTIVOS`, o fim de jogo e as teclas |
| `docs/adr/` | sem ADR novo: 0002 (snapshot completo, o cliente não pergunta) e 0004 (só Textual) já decidem; a tradução de motivo é de tela, não de fio |

Consumidor imediato: as quatro pessoas do roteiro — em uma máquina ou em duas — que hoje leem `fora_de_hora` e não sabem o que aconteceu.

## Não objetivos

- Recomeçar a série depois das 4 partidas: a tela mostra o fim e para aí; mesa nova é `restart` do servidor (Q3 do grill da 05, fora do v1).
- Bloquear as teclas de jogada com a mesa **congelada**: a recusa continua sendo do servidor (`mesa_congelada`, `docs/adr/0001`), como decidiu a 06 (decisão 4 do grill). Com a mesa **encerrada** o cliente para de mandar `jogar` (decisão 12): `encerrado` é estado terminal do snapshot, não regra de jogo calculada na tela — a mesma natureza do guard de mão vazia (`main.py:200-202`).
- Traduzir os motivos no servidor ou no `protocolo.py`: o fio segue em código estável; a frase é decisão de tela.
- Traduzir `ErroJogada`/`motivo` para `Enum` novo ou `StrEnum` no protocolo: o dicionário de tela basta e não mexe no codec da 04.
- Um tema próprio, CSS extenso ou widget novo: ADR 0004 e o teto de `80x24` do PLANO; o tema é o `textual-light`/`textual-dark` do Textual.
- `notify`/toast do Textual para o erro: o `#aviso` já é o painel da mensagem (`main.py:249`); trocar por toast muda o teste sem mudar a experiência.
- Autenticação, TLS, descoberta automática do servidor na rede: fora do v1 (`docs/adr/0002`); o passo a passo entre duas máquinas é `--host` na mão.
- Documentar o jogo em `CONTEXT.md`: nenhum vocabulário novo entra — dupla, partida e jogo já estão lá.

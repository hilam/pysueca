# Design — Sprint 02 — Vaza e mão

> **Sprint:** `sprints/02-vaza-e-mao/` — decisão do PLANO: `Mao` como máquina de estados explícita (`preparar` → 10 vazas → `pontuar`), com `puxar`/`jogar` devolvendo erro em vez de exceção para jogada ilegal, sobre o RNG injetado na sprint 01.
> **Depende de:** Sprint 01 — Carta e baralho (concluída)

## Contexto

Existem `src/pysueca/carta.py` (`Naipe`, `Valor`, `Carta`, `Carta.vence`) e `src/pysueca/baralho.py` (`Baralho(rng)`, `embaralhar()`), provados por `tests/test_carta.py` (20 testes, 100% de cobertura). Não existe motor de jogo. Esta sprint cria `src/pysueca/motor.py` com a vaza e a mão, ainda sem rede e sem UI (`docs/adr/0004`).

## Objetivos / Não objetivos

**Objetivos:**
- `src/pysueca/motor.py`: `Vaza` (naipe puxado, trunfo, jogadas, vencedor), `Mao` (`preparar` → 10 vazas → pontuação), `ErroJogada` e `Resultado`.
- `tests/test_motor.py` verde, jogando uma mão inteira com cartas legais ao acaso e provando a obrigação de naipe, o trunfo, a vez, a distribuição e o resultado.
- Reusar `Carta.vence` (sprint 01) e `Baralho(rng)` como estão — nenhuma mudança nos módulos da sprint 01.

**Não objetivos:**
- `Jogo` (partidas, placar acumulado, rotação de papéis) — sprint 03. Aqui `embaralhador` é um parâmetro.
- Protocolo de fio, snapshot, validação de rede — sprints 04–05.
- Ordem da distribuição "cima/baixo": modelada só como a ponta do baralho (primeira ou última carta).
- "Cortar o baralho" e a interação pergunta/resposta: o corte não altera o resultado no modelo reduzido; a resposta entra como `cima: bool`.
- Tela: as cartas continuam em texto de fio (`"7H"`); o símbolo colorido é sprint 06.

## Decisões

**1. `Vaza` separada de `Mao`, reusando `Carta.vence`.**
Critério: o desempate par a par já é `Carta.vence(outra, naipe_puxado, trunfo)` (`carta.py:85`, provado em `tests/test_carta.py:56-83`). `Vaza.vencedor` é a redução dessa comparação sobre as jogadas — nenhuma regra de precedência é reescrita. Alternativa rejeitada: refazer o `peso()` dentro de `motor.py`; duplicaria a única fonte da ordem trunfo > naipe puxado > descarte. Por isso os cenários "entre trunfos vence a maior" e "maior força do naipe puxado vence os descartes" já nascem verdes: são cobertura da agregação, não regra nova (lição da sprint 01: não inventar implementação pior só para forçar vermelho).

**2. `puxar` fundido em `jogar` — por que X e não Y.**
Critério: o PLANO escreve `puxar`/`jogar`, mas a única mensagem de rede é `jogar` (sprint 04, entregável lista `entrar`/`responder`/`jogar`/`estado`). Quem puxa ou segue é decidido pelo estado (`self.vaza is None`), não pelo chamador — separar em dois métodos criaria um `puxar` sem consumidor no servidor e um precondição que o cliente não conhece. `Mao.jogar(assento, carta)` cobre os dois casos; confirmado no grill, sem wrapper de `puxar`.

**3. Jogada ilegal devolve `ErroJogada`, não levanta.**
Critério: é a decisão do PLANO e da ADR 0001 — o servidor não pode derrubar a mesa por causa de um cliente. `class ErroJogada(enum.Enum)` com `FORA_DA_VEZ`, `CARTA_FORA_DA_MAO` e `NAO_SEGUIU_NAIPE`; `Mao.jogar` devolve `ErroJogada | None`. Não é `erro` genérico porque o servidor (04/05) precisa distinguir os casos para a mensagem ao cliente. Alternativa rejeitada: exceção (`ValueError`); obrigaria o servidor a capturar exceção por jogada.
Fronteira com o protocolo (grill): o motor é dono dos erros de regra — vez, posse e naipe — e `protocolo.py` (sprint 04) é dono dos erros de fio (tipo desconhecido, campo faltando, teto de bytes, nome) e apenas formata o `ErroJogada` recebido; nenhuma checagem de regra duplicada no protocolo.

**4. Preparação reduzida: o trunfo é a ponta do baralho.**
Critério: `carta_trunfo = cartas.pop(0 if cima else -1)`; o dador é `(embaralhador + 3) % 4` (README item 3, com A=0 → dador D=3) e recebe a carta. O resto é distribuído em rodízio entre os assentos, 9 cartas para o dador + a do trunfo = 10. Cortador (`(e+2)%4`) e respondente (`(e+1)%4`) não são modelados: o corte não altera o resultado e a resposta vira o parâmetro `cima`. Alternativa rejeitada: modelar a ordem da distribuição item 5.1/5.2 do README — observável apenas por quem fica com a carta do trunfo (risco declarado no PLANO), custo sem teste que o distinga.

**5. Uma `Mao` por mão; o baralho é criado em `preparar`.**
Critério: `Mao(embaralhador, rng=None)` guarda o RNG e cria `Baralho(self.rng)` dentro de `preparar(cima=True)`; assim `preparar` pode ser reexecutado (novo baralho) e o RNG determinístico continua valendo. Alternativa rejeitada: `Mao` receber um `Baralho` pronto — obrigaria `Jogo` (03) a construir o baralho e a guardar o RNG em dois lugares.

**6. `Resultado.de_pontos` puro, apontado por `Mao.resultado`.**
Critério: os limites 60/61/90/91/119/120 precisam de teste de fronteira sem jogar 10 vazas. `Resultado.de_pontos(dupla_0_2, dupla_1_3)` classifica um placar fechado; `Mao.pontos` devolve a tupla por dupla (`assento % 2`) e `Mao.resultado` chama o classificado. Sem guarda de "mão incompleta": `pontos`/`resultado` só são significativos depois das 10 vazas e testar placar parcial não é requisito. `Resultado` fica só com a classificação da mão; `partidas` (4/2/1/0) e a dupla vencedora são da sprint 03, quando `Jogo` acumular o placar — confirmado no grill.

**7. `jogada_legal` como função, não método.**
Critério: a obrigação é uma propriedade de `(mão, naipe_puxado, carta)` e é usada só por `Mao.jogar`; como função pura é testável à parte do estado. Rejeitada a validação espalhada em `puxar`/`jogar` (decisão 2).

**8. `Mao` expõe `maos`, `vaza`, `vazas`, `vez`, `trunfo`, `carta_trunfo`, `pontos`, `resultado`.**
Critério: o snapshot completo do protocolo (ADR 0002, sprint 04) precisa de tudo isso; não há campo especulativo. Não expor `self.baralho` (já consumido) nem a ordem da distribuição.

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| Regra de trunfo reinterpretada no `motor.py` e divergir de `carta.py` | `Vaza.vencedor` só chama `Carta.vence`; teste V4 âncora o reuso |
| Distribuição "cima/baixo" impossível de observar | modelo reduzido: só a ponta do baralho; teste com seed comparando com `Baralho(random.Random(42))` embaralhado |
| Dador errado (parceiro em vez de adversário) e trunfo na mão errada | teste M2 fixa embaralhador 0 → dador 3 (README item 3) |
| Jogada ilegal mutar o estado por validação fora de ordem | validar tudo antes de qualquer mutação; teste M10 audita mão/vez/vaza |
| `peso` divergente no desempate de descartes | V6 usa a vaza de 4 cartas com Ás de paus descartado |

## Plano de Migração

N/A — código novo, nenhuma API pública anterior além de `carta.py`/`baralho.py`, que não mudam. Rollback é apagar `motor.py` e `tests/test_motor.py`. Nenhuma dependência nova (`docs/adr/0004`).

## Questões Abertas

Nenhuma pendência — as quatro foram fechadas no grill:

- `docs/adr/0002` mal citada no PLANO: sem ADR nova (a distribuição reduzida é simplificação de teste, não decisão arquitetural); o PLANO passa a apontar `docs/adr/0003`.
- `puxar` fundido em `Mao.jogar` — confirmado (decisão 2).
- `pontos`/`resultado` antes das 10 vazas sem guarda — confirmado (decisão 6).
- Erros de regra no motor e erros de fio no protocolo, sem duplicação — confirmado (decisão 3).

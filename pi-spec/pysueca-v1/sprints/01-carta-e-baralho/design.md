# Design — Sprint 01 — Carta e baralho

> **Sprint:** `sprints/01-carta-e-baralho/` — decisão do PLANO: separar `carta.py` de `motor.py`; o RNG é injetado (`random.Random` com default próprio, nunca o global). Ver `docs/adr/0004`.
> **Depende de:** nenhuma

## Contexto

O repositório tem só o esqueleto Textual (`src/pysueca/main.py`, 57 linhas, substituído na sprint 06), 40 PNGs sem uso (`src/pysueca/imagens/`) e `pyproject.toml` com Textual e dev-tools. Não existe `tests/`, `AGENTS.md` nem código de regra. O motor puro começa aqui.

## Objetivos / Não objetivos

**Objetivos:**
- Criar `src/pysueca/carta.py` como **única** fonte da aritmética de carta: pontos, força, texto `"7H"` ida-e-volta e desempate com trunfo.
- Criar `src/pysueca/baralho.py` com as 40 cartas e embaralhamento determinístico sob RNG injetado.
- Provar tudo em `tests/test_carta.py` sem rede, sem `asyncio` e sem Textual.
- Criar `AGENTS.md` com comandos, mapa de arquivos e invariantes.

**Não objetivos:**
- `motor.py` (`Mao`/`Jogo`) — sprints 02–03; esta sprint só entrega a aritmética que eles consomem.
- Distribuição "cima/baixo" — sprint 02.
- Protocolo de fio e rede — sprints 04–05.
- Render `A♥` — sprint 06.
- Corrigir o entrypoint quebrado (`pyproject.toml:12`) — sprint 06 substitui `main.py`.

## Decisões

**1. `carta.py` separado de `motor.py` — por que X e não Y.**
Critério: a aritmética de carta é consumida por três pontos distintos — o motor (sprint 02), o protocolo (sprint 04, que traduz `"7H"` em carta) e os testes. Manter em `motor.py` acoplaria o protocolo ao motor só para ler `de_texto`. Alternativa rejeitada: classe dentro de `motor.py`; custo é import cycle futuro.

**2. Força e pontos independentes.**
Critério: os pontos não derivam a força — Seis, Cinco, Quatro, Três e Dois valem todos 0 mas têm força decrescente. Alternativa rejeitada: ordenar por pontos (empata os zeros). `Valor` carrega `pontos: int` e `forca: int` como dados, não como cálculo.
Glossário: `CONTEXT.md` define "Valor" como a face/pontuação da carta e marca "força" como termo a evitar; aqui **força** é o desempate da vaza (`A > 7 > K > J > Q > 6 > 5 > 4 > 3 > 2`), não sinônimo de Valor — é o sentido que o PLANO usa.

**3. `Naipe` e `Valor` como `enum.Enum`.**
Critério: os 14 símbolos são fechados e as cartas são hasháveis/comparáveis por identidade; `str` cru deixaria `"copas"`/`"H"`/`"♥"` circularem como três representações. `enum` é stdlib (`docs/adr/0004`).

**4. Desempate em `carta.py`, não em `motor.py`.**
Critério: a regra "trunfo > naipe puxado > descarte" é aritmética de carta — recebe `(outra, naipe_puxado, trunfo)` e devolve `bool`, sem conhecer assento, mão ou vaza. A assinatura sem `naipe_puxado` seria incorreta num vaza de três naipes: puxado = Rei de copas, descarte = Ás de paus venceria o naipe puxado por força. Alternativa rejeitada: deixar o `motor.py` (sprint 02) desempatar o naipe puxado — dividiria a regra em dois módulos. Exposto como `Carta.vence(outra, naipe_puxado, trunfo) -> bool`.

**5. RNG injetado.**
Critério: testes precisam de cenário concreto ("o assento 2 ficou com o Ás de trunfo"), não só invariantes; e o `random` global é estado mutável compartilhado entre testes. Assinatura: `Baralho(rng: random.Random | None = None)`, criando `random.Random()` quando `None`. Alternativa rejeitada: `random.seed()` global no teste — vaza para toda a sessão de pytest.

**6. Texto `"7H"` (fio) ≠ render `A♥` (tela).**
Critério: o protocolo (sprint 04) precisa de um formato estável que caiba numa linha JSON; o símbolo colorido é decisão de UI (`docs/adr/0004`, sprint 06). `Carta.de_texto`/`texto()` ficam no formato de fio; a TUI formata o símbolo a partir do `Naipe`/`Valor`. Sem `Carta.__str__`: `texto()` é o único renderizador de fio, e não há dunder de formatação a manter.

**7. `AGENTS.md` gerado nesta sprint como task de documentação.**
Critério: é o entregável do PLANO e as sprints 02+ dependem de comandos e invariantes documentados. Não vira capability nem spec: testar prosa é teste frágil e a conferência é humana. Conteúdo: `uv run`, mapa de arquivos, as invariantes "motor puro e síncrono" e "só Textual", ponteiro para `docs/adr/`.

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| Ordem de força invertida ou trocada (`A > 7 > K > J > Q > 6…`) | teste tabelado cobrindo os 10 valores, não amostra |
| `random` global vazando para o baralho | default cria instância própria; teste de determinismo por seed |
| `Valor` (glossário = pontos) confundido com força | `CONTEXT.md` é canônico; nomes `pontos`/`forca` explícitos |
| Texto de fio divergir do que o protocolo espera (sprint 04) | formato fechado nesta spec e reusado em `de_texto`/`texto()` |
| Desempate ignorar o naipe puxado e fazer um descarte de força maior vencer | assinatura `vence(outra, naipe_puxado, trunfo)` com teste do cenário de três naipes |

## Plano de Migração

N/A — código novo, nenhuma API pública anterior, nenhuma dependência nova (`pyproject.toml` intocado). Rollback é apagar os arquivos novos.

## Questões Abertas

- `pyproject.toml:12` (`pysueca = "pysueca:src.pysueca.main"`) aponta para módulo inexistente. Corrigir na sprint 06, que substitui `main.py`? (recomendação: sim)

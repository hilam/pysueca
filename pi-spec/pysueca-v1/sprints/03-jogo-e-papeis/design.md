# Design — Sprint 03 — Jogo e papéis

> **Sprint:** `sprints/03-jogo-e-papeis/` — decisão do PLANO: `Jogo` acumula partidas por dupla e encerra ao chegar a 4 partidas (a bandeira, que vale 4, cai nessa regra); a rotação de embaralhador/cortador/dador anda um assento por mão.
> **Depende de:** Sprint 02 — Vaza e mão (concluída)

## Contexto

`src/pysueca/motor.py` já tem `Vaza`, `Mao`, `ErroJogada` e `Resultado` (`motor.py:29-128`), provados por `tests/test_motor.py` (18 testes, 100% de cobertura de `motor.py`). A `Mao` recebe um `embaralhador` fixo no construtor e não sabe de placar nem de mão seguinte. O `Resultado` classifica limites (`de_pontos`, `motor.py:54`) mas não diz quantas partidas a mão vale — a sprint 02 deixou isso explicitamente para cá. `Jogo` não existe.

Esta sprint fecha o motor: `Jogo` passa a ser o dono da `Mao` corrente, do placar e do fim da mesa, ainda sem rede e sem UI (`docs/adr/0004`).

## Objetivos / Não objetivos

**Objetivos:**
- `src/pysueca/motor.py`: `Jogo` (`preparar` → `jogar` × 10 vazas → `encerrar_mao` → próxima mão ou fim) e `Resultado.partidas`.
- `tests/test_jogo.py` verde, provando a rotação de papéis, o acúmulo por dupla, o empate 60–60, a bandeira encerrando na hora e o limite de 4 partidas.
- Reusar `Mao` como está — a vaza, a jogada ilegal e a pontuação não mudam.

**Não objetivos:**
- Serialização, snapshot e validação de rede — sprint 04.
- `asyncio`, servidor, reconexão — sprint 05.
- Tela, placar desenhado, mensagem de fim de jogo — sprint 06–07.
- Modelar cortador e respondente como estado: a `Mao` já os deriva do embaralhador (decisão 4 da sprint 02); rodar o embaralhador roda os três papéis.
- Sortear o primeiro embaralhador dentro do motor (ver decisão 6).

## Decisões

**1. `Jogo` mora em `motor.py`, não num `jogo.py` novo.**
Critério: `Jogo` é regra pura e síncrona, como `Vaza`/`Mao`, e o `AGENTS.md:26` trata `motor.py` como o módulo de regra ("o futuro `motor.py`"). Um arquivo separado só se justificaria por tamanho, e `motor.py` fica em ~170 linhas. Alternativa rejeitada: `src/pysueca/jogo.py` — criaria um terceiro import de regra sem fronteira própria e dividiria `Resultado`/`ErroJogada` entre arquivos.

**2. `Jogo` é dono da `Mao` corrente e delega `jogar`.**
Critério: o servidor (05) precisa de um dono único do estado da mesa (ADR 0001). `Jogo.jogar(assento, carta)` devolve `ErroJogada | None` repassando `Mao.jogar` — a validação continua toda no motor da sprint 02, sem duplicação. Alternativa rejeitada: `Jogo` só somar placar e o servidor guardar a `Mao` — espalharia o estado da mesa por dois donos.

**3. `encerrar_mao()` é explícito; `jogar` não fecha a mão sozinho.**
Critério: cada mão precisa da resposta "cima ou baixo" do respondente antes da distribuição (`README.md:32,38`), e a `Mao` só a recebe em `preparar(cima)`. Se `jogar` criasse a mão seguinte ao fechar a décima vaza, ele teria que prepará-la sem a resposta — inventando um `cima` que ninguém deu. Com `encerrar_mao()` separado, o servidor anuncia o resultado da mão, pergunta de novo e chama `preparar(cima)`. O contrato é `encerrar_mao() -> Resultado` (confirmado no grill): o servidor anuncia o desfecho da mão sem depender de ler `Jogo.mao.resultado` antes da rotação. Alternativa rejeitada: `Jogo.jogar` detectar `len(mao.vazas) == 10` e rotacionar sozinho, abrindo a próxima mão sem partida ainda preparada.

**4. `Resultado.partidas` é propriedade do enum, não mapa no `Jogo`.**
Critério: quem sabe que quilo vale 2 é o `Resultado`, do mesmo jeito que `de_pontos` sabe os limites (`motor.py:54`); o mapa fica junto da classificação que ele completa. A sprint 02 delegou explicitamente `Resultado.partidas` (4/2/1/0) a esta sprint (`qa-plan.md` da 02, "Delegado à sprint 03"). Alternativa rejeitada: dicionário local em `Jogo` — a aritmética de pontuação ficaria partida em dois lugares.

**5. Empate de 60 a 60 curto-circuita, sem computar dupla vencedora.**
Critério: `EMPATE` vale 0 e não tem vencedor; calcular a dupla e somar 0 tocaria a dupla errada por acidente (`pontos[0] > pontos[1]` é falso no empate). O `encerrar_mao` devolve cedo no empate, e o EDGE 60–60 executa esse ramo e ancora o placar parado. Alternativa rejeitada: `self.partidas[dupla] += 0` — funciona por acidente e esconde que empate não tem vencedor. Nota: o curto-circuito não é observável no placar (somar 0 não muda nada), então o EDGE é cobertura do ramo, não um RED independente.

**6. O primeiro embaralhador é parâmetro, default 0 (A); o motor não sorteia.**
Critério: `README.md:30` fixa A na primeira mão; o `CONTEXT.md:56` diz "na primeira mão é sorteado", mas o motor da sprint 01 decidiu por RNG injetado e parâmetros explícitos em vez de sorteios escondidos (design da sprint 01, decisão do RNG). `Jogo(rng, embaralhador=0)` é determinístico por padrão; quem quiser sortear passa o assento sorteado (o servidor pode fazê-lo). Alternativa rejeitada: `randrange(4)` dentro do construtor — esconderia o consumo do RNG e dificultaria o teste de "o embaralhador puxa a primeira vaza".

**7. A rotação acontece em `encerrar_mao`, junto da abertura da mão seguinte.**
Critério: `encerrar_mao` soma o placar, decide o fim e, se o jogo continua, anda o embaralhador `(e+1)%4` e cria a nova `Mao`. `preparar(cima)` só prepara a `Mao` corrente. Assim `Jogo.embaralhador` e `Jogo.mao.embaralhador` nunca divergem depois de `encerrar_mao`. Alternativa rejeitada: rotacionar dentro de `preparar` — o placar teria que saber "houve mão anterior?", virando estado extra.

**8. Fim do jogo é `max(partidas) >= 4`; bandeira cai nessa mesma regra.**
Critério: o README (linha 54) diz que ganha quem faz 4 partidas primeiro, e a bandeira vale exatamente 4 (`specs/mao`), então uma regra só cobre os dois casos e a bandeira "encerra na hora" por consequência. Alternativa rejeitada: tratar `BANDEIRA` como caso especial de encerramento — duplicaria a condição e poderia encerrar em 4 por dois caminhos divergentes.
O quilo vale 2 e **não** encerra por si: a linha 24 ("Bandeira e quilo encerram o jogo na hora") contradiz a corrida até 4 partidas e a tabela de pontos (`README.md:47-54`). **Confirmado no grill**: só 4 partidas encerram, e `README.md:24,54`/`CONTEXT.md:90` recebem errata para remover o quilo.

**9. `Jogo` expõe `partidas`, `embaralhador`, `mao`, `encerrado` e `vencedor`.**
Critério: o snapshot completo do protocolo (ADR 0002, sprint 04) precisa do placar e do estado da `Mao`; a tela final (06) precisa de `encerrado`/`vencedor`. `vencedor` é `None` enquanto o jogo corre e a dupla que alcançou 4 quando encerra — uma linha, já que `max(partidas)` é único (só o vencedor da mão soma, e paramos em 4). Nenhum campo é especulativo.

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| README afirma que quilo também encerra (`README.md:24,54`) e a implementação só encerra em 4 | regra única `>= 4` confirmada no grill, com errata em `README.md`/`CONTEXT.md`; o quilo encerrando seria incompatível com "corrida até 4 partidas" e com a tabela (quilo = 2) |
| Testar bandeira/60–60/4 partidas exigiria jogar muitas mãos reais | teste usa uma `Mao` de placar fixo (subclasse só no teste, sem fábrica no motor); a rotação e a mão inteira continuam testadas com `Mao` real e RNG determinístico |
| `encerrar_mao` chamado com a mão incompleta somaria placar parcial | contrato documentado: `encerrar_mao` fecha uma mão de 10 vazas; o servidor (05) só o chama ao fechar a décima, como `pontos`/`resultado` na sprint 02 |
| `embaralhador` do `Jogo` divergir do da `Mao` | rotação e criação da nova `Mao` juntas em `encerrar_mao`; teste de rotação compara os dois |
| Empate somar partida à dupla errada | curto-circuito do empate antes de calcular a dupla (decisão 5); EDGE 60–60 ancora |

## Plano de Migração

N/A — código aditivo no `motor.py` (uma propriedade em `Resultado` e a classe `Jogo`). Nenhuma API pública anterior muda; `carta.py`, `baralho.py` e a `Mao` ficam intactos. Rollback é apagar `Jogo`/`Resultado.partidas` e `tests/test_jogo.py`. Nenhuma dependência nova (`docs/adr/0004`).

## Questões Abertas

Nenhuma pendência — as três foram fechadas no grill:

- Quilo **não** encerra o jogo: só 4 partidas encerram, e a bandeira (4) cai nessa regra; `README.md:24,54` e `CONTEXT.md:90` recebem errata (decisão 8).
- `Jogo.vencedor` entra nesta sprint: é regra de jogo, não de tela; a TUI (06) só lê (decisão 9).
- `encerrar_mao()` devolve `Resultado`: o servidor (05) anuncia o desfecho sem depender da ordem "ler antes de encerrar" (decisão 3).

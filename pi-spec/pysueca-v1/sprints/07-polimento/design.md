# Design — Sprint 07 — Polimento

> **Sprint:** `sprints/07-polimento/` — decisão do PLANO: "N/A — ver `sprints/07-polimento/design.md`" (`PLANO-PYSUECA-V1.md:87`)
> **Depende de:** Sprint 06 — Cliente TUI (concluída)

## Contexto

A 06 fechou a mesa funcional: o cliente desenha o snapshot, manda intenções e mostra queda e erro no `#aviso` (`main.py:244-270`). O que ficou de propósito para a 07 (não objetivos da 06):

- os motivos de `erro` aparecem como código de fio — `fora_de_hora`, `nome_em_uso`, `json_invalido`, `mesa_congelada` (`tests/test_cliente.py:319-321,477-481,490-493,551-553`);
- `encerrado` e `vencedor` chegam no snapshot (`protocolo.py:47-64`) e a tela ignora os dois: `desenhar_mesa` mostra só `Placar: 0 x 0` (`main.py:67`) e `texto_aviso` ainda anuncia "Sua vez" com a mesa encerrada, porque `vez` continua preenchido depois da última vaza (`main.py:262-266`);
- o `d`/`action_toggle_dark` saiu com o esqueleto e as três teclas de jogo são `show=False` (`main.py:115-117`), então o rodapé anuncia só `Sair`;
- o `README.md` ensina quatro terminais na mesma máquina (`README.md:64-81`) e não menciona `--host 0.0.0.0`, o que deixa o jogo entre duas máquinas impossível na prática (o default é `127.0.0.1`, `servidor.py:196-197`).

## Objetivos / Não objetivos

**Objetivos:**
- motivo de recusa em frase de jogador, com fallback que não derruba a tela;
- fim do jogo na mesa, com o placar final e a dupla vencedora, sem anúncio de vez e sem a tecla de jogar mandar `jogar`;
- `d` de volta ao tema claro/escuro; teclas de jogo visíveis no `Footer`;
- `README.md` com o v1 pronto e o passo a passo entre duas máquinas.

**Não objetivos:**
- recomeçar a série, autenticação, TLS, segunda mesa, modo imagem (proposal → Não objetivos);
- criar ADR: nenhuma decisão desta sprint muda protocolo, invariante ou dependência (0002 e 0004 já cobrem).

## Decisões

**1. A tradução do motivo mora no cliente, não no `protocolo.py`.**
- *X*: `MOTIVOS` em `main.py`, aplicado em `avisar`.
- *Y*: traduzir em `protocolo.py` (no `Erro`) ou no `servidor.py`.
- *Critério*: o fio é contrato sem humanidade (`docs/adr/0002`: snapshot completo, código estável) e o `servidor.py` não conhece a língua do jogador; o cliente é a única fronteira humana e já é dono da tradução fio→tela (invariante da 06, `AGENTS.md`). Traduzir no protocolo ainda poluiria o `desserializar`, cujo retorno é mensagem de fio, não texto de tela.

**2. Dicionário fixo de frases com fallback genérico, não frase montada do código.**
- *X*: `MOTIVOS: dict[str, str]` com os motivos do v1 e um fallback ("A mesa recusou o pedido").
- *Y*: `motivo.replace("_", " ")` + capitalize — uma linha, cobre motivo desconhecido de graça.
- *Critério*: a experiência é o motivo da sprint; o `replace` não tem acento nem voz de jogador (`nao segue naipe` vs "você precisa seguir o naipe puxado"). O fallback cobre o motivo novo sem quebrar a tela, que é o único requisito real de robustez. O `replace` fica como saída de emergência se o grill achar o dicionário grande demais.

**3. O fim do jogo aparece no painel da mesa, não no `#aviso` nem num modal.**
- *X*: linha de fim em `desenhar_mesa` (`main.py:56-71`), que já é o painel do placar.
- *Y1*: `#aviso` — é o painel do transitório (queda > erro > vez) e a mesa encerrada é permanente.
- *Y2*: `ModalScreen` — bloquearia a leitura da mesa final e exigiria tecla de saída.
- *Critério*: o painel que já mostra `Placar: X x Y` é o dono natural do placar final; nenhum widget novo.

**4. A vez é silenciada na tela, não no snapshot.**
- *X*: `texto_aviso` não anuncia vez quando `estado.encerrado`.
- *Y*: zerar `vez` em `protocolo.estado` quando o jogo terminou.
- *Critério*: `vez` é verdade do motor (a última vaza tem vencedor) e `estado()` é protocolo puro; suprimir na tela mantém a mesma fronteira da decisão 1 e não muda o fio da 04/05.

**5. `Footer` com `show=True` nos três bindings, sem widget de ajuda.**
- *X*: tirar o `show=False` de `left`/`right`/`enter` (`main.py:115-117`).
- *Y*: um `Static` ou `HelpPanel` caseiro com a lista de teclas.
- *Critério*: o `Footer` já existe no `compose` (`main.py:130-137`) e o teto do PLANO é `80x24`; um painel de ajuda custaria altura e widget novo sem ganho (`docs/adr/0004`).

**6. O tema é o `action_toggle_dark` do Textual.**
- *X*: `Binding("d", "toggle_dark", …)` e o action da biblioteca.
- *Y*: tema próprio em `App.CSS`/`textual.tcss`.
- *Critério*: ADR 0004 (só Textual; nada de tema próprio) e o esqueleto removido na 06 já usava esse action. Em Textual 8.2.8 o action troca `app.theme` entre `textual-dark` e `textual-light` — **`app.dark` não existe mais**; o teste assevera `app.theme` (medido, não suposto).

**7. O teste do rodapé lê os `FooterKey`, não a declaração.**
- *X*: `app.query(FooterKey)` e a lista de `(tecla, descrição)` visíveis.
- *Y1*: asseverar `Binding.show` na classe — testa a declaração, não o rodapé.
- *Y2*: `Footer.render()` — no `run_test` devolve `Blank` (medido: o `Footer` do app atual não tem texto renderizado; as teclas vivem nos filhos `FooterKey`).
- *Critério*: o `FooterKey` é o render real e lê os bindings ativos; se alguém voltar o `show=False`, o teste fica vermelho.

**8. Duas máquinas com `--host 0.0.0.0` documentado, sem flag nova.**
- *X*: `README.md` ensina `pysueca-servidor --host 0.0.0.0` e clientes com `--host <ip>`.
- *Y*: flag `--publico` no servidor que liga o bind público.
- *Critério*: `--host` já existe (`servidor.py:196-197`, spec `comando` da 06); flag nova seria código para documentação (YAGNI) e uma segunda fonte de verdade para o mesmo bind.

**9. A frase do motivo fala da ação recusada, não do estado da mesa.**
- *X*: a frase de `mesa_congelada` descreve a jogada que caiu por causa do congelamento.
- *Y*: deduplicar em `texto_aviso` — omitir a frase quando `ausentes` não está vazio.
- *Critério*: o banner de queda já diz o estado (quem caiu) e a jogada recusada precisa do seu retorno visível; a diferença sai de graça no texto, sem `if` novo no renderizador.

**10. A dupla vencedora é nomeada, com fallback para o índice.**
- *X*: `Ana e Caio` quando os dois nomes existem em `assentos`; `dupla 0–2`/`dupla 1–3` quando algum está ausente.
- *Y*: só o índice de assento, sem depender de `assentos`.
- *Critério*: o público da sprint é quem não escreveu o código e o caso do nome ausente é real (queda na última mão); a expressão condicional é a mesma linha de código.

**11. O `d` aparece no rodapé.**
- *X*: `Binding("d", "toggle_dark", "Tema")` visível, como as teclas de jogo.
- *Y*: `show=False`, com o `README.md` como única descoberta.
- *Critério*: a sprint é sobre teclas descobríveis e os cinco itens cabem em `80x24`; o `show=False` esconderia justamente a tecla que a 06 removeu por engano.

**12. A mesa encerrada para de mandar jogada.**
- *X*: somar `estado.encerrado` ao guard de `action_jogar` (`main.py:200-202`), como o guard de mão vazia.
- *Y*: seguir mandando e deixar o servidor recusar.
- *Critério*: `encerrado` vem do snapshot, não é regra de jogo calculada no cliente (ADR 0001 intacto); mandar ao fim da mesa faria o jogador ler `fora_da_vez` como resposta — o guard evita uma mensagem enganosa com uma condição.

**13. O `MOTIVOS` cobre todos os códigos do v1.**
- *X*: os ~16 códigos (`protocolo.py:166-181`, `servidor.py:71-122`, `ErroJogada` em `motor.py:13-18`), com o fallback só para motivo novo.
- *Y*: só os que um jogador sentado pode ver; `campo_extra`/`tipo_desconhecido` cairiam no genérico.
- *Critério*: é uma tabela de texto; cobrir tudo torna o teste do enum do motor uma garantia de verdade (motivo novo do motor sem frase fica vermelho) e o genérico passa a significar "novidade", não "esquecimento".

**14. O comando que descobre o IP da mesa fica delegado à implementação.**
- *X*: o `README.md` cita o comando (`hostname -I` ou equivalente) ao lado do `--host`.
- *Y*: fixar o comando exato no artefato agora.
- *Critério*: é uma linha de prosa que depende da máquina do leitor (Linux/macOS/Windows); o grill não gasta rodada com isso e o texto final é da implementação.

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| Quatro testes da 06 asseguram o código cru e ficam vermelhos de propósito | a troca do assert entra no mesmo ciclo RED→GREEN do `MOTIVOS` (task do bloco 3); a suite tem de estar verde no commit, não "consertada depois" |
| Fallback genérico esconde um motivo novo sem tradução | o fio cru continua inspecionável (`nc localhost 8765`, risco global do PLANO) e o `Erro` do protocolo segue com o código no fio; nenhuma informação se perde no protocolo, só na tela |
| Frase de `mesa_congelada` duplicando o banner de queda no mesmo `#aviso` | resolvido na decisão 9: a frase fala da ação recusada e o banner do estado, então as duas dizem coisas diferentes e nenhum `if` de dedup entra |
| `d` colidindo com tecla de jogo ou com o modal | `d` não colide com `←`/`→`/`Enter`/`c`/`b`, e a tela modal é quem tem foco enquanto o cima ou baixo está aberto |
| Dupla vencedora com `assentos` incompleto (`None`) | resolvido na decisão 10: `vencedor` é índice de dupla (0 ou 1), os nomes entram quando existem e o fallback é `dupla 0–2` |
| `encerrado` com `vencedor` nulo (impossível no servidor v1, o campo vem sempre preenchido) | guard defensivo de uma linha, sem RED independente — lição das sprints 01–03: não declarar vermelho para o que a implementação adjacente cobre |
| `app.dark` não existe no Textual 8.2.8 e o teste do tema escrito de memória falharia | o teste assevera `app.theme` (`textual-dark`/`textual-light`), medido no ambiente da sprint |

## Plano de Migração

N/A — não há protocolo novo, estado persistido, dado de usuário nem dependência. O que muda é tela e prosa do `README.md`; o rollback é reverter o commit.

## Questões Abertas

Nenhuma — o grill de 2026-10-12 fechou as seis. Resoluções nas decisões 2 (fallback genérico puro) e 9–14.

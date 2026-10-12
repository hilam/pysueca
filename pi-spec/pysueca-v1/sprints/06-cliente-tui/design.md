# Design — Sprint 06 — Cliente TUI

> **Sprint:** `sprints/06-cliente-tui/` — decisão do PLANO: a leitura do socket é um worker asyncio do Textual que só traduz mensagem em método de tela, e nenhum widget conhece o protocolo; cartas em texto com naipe colorido (ADR 0004).
> **Depende de:** Sprint 05 — Servidor (concluída); o fatiamento do PLANO permite desenvolver os widgets contra um servidor falso, como esta sprint faz.

## Contexto

O v1 está completo do lado de baixo: `Carta`/`Baralho` (01), `Vaza`/`Mao`/`Jogo` (02–03), o codec JSON linha a linha com validação estrita (04) e o `Servidor` que é a mesa (05) — 100% de cobertura nas duas últimas, provados por robôs de verdade em `asyncio`. O que falta é a ponta humana. `src/pysueca/main.py` é o esqueleto de 57 linhas: `SuecaApp` com `Header` e `Footer` e um `Container` vazio (`main.py:41`), constantes de naipe/carta em inglês sem uso e `PATH_IMAGENS` apontando para uma pasta que nem existe mais (`main.py:19`); `uv run mypy src` está vermelho desde a sprint 01 por causa de `main.py:52`. O `pyproject.toml:12` declara `pysueca = "pysueca:src.pysueca.main"`, que não resolve para módulo nenhum — o entrypoint quebrado que o PLANO carrega desde a visão geral e que a 05 deixou explicitamente para esta sprint. Não há como subir o servidor por linha de comando, então o "roteiro manual de 4 terminais" do entregável não tem como existir antes desta sprint.

A decisão 1 do design da 05 fechou a fronteira: `servidor.py` é a única casca `asyncio` **que possui a mesa**. Esta sprint acrescenta a segunda e última casca `asyncio` do projeto — o cliente — sem tocar no motor, no protocolo nem na mesa.

## Objetivos / Não objetivos

**Objetivos:**
- `src/pysueca/main.py`: `SuecaApp(host, porta, nome)`, o worker de leitura do fio, os painéis de assentos/mesa/mão/aviso, as ações de tecla e o diálogo cima ou baixo — nenhum widget sabendo o que é `Estado` ou `Erro`.
- `tests/test_cliente.py` verde com `App.run_test()` contra um servidor falso roteirizado, cobrindo ida-e-volta de `entrar`, espera `N de 4`, mão colorida, seleção `←`/`→`/`Enter`, diálogo cima ou baixo, queda, erro e parsing da linha de comando.
- `main(argv)` do cliente e `main(argv)` do servidor, com `argparse` e defaults `127.0.0.1:8765`, fechando `pyproject.toml:12` e adicionando `pysueca-servidor`.
- `README.md`: o roteiro de 4 terminais.

**Não objetivos:**
- Traduzir motivo de `erro`, placar final, teclas no `Footer` e bind para duas máquinas — sprint 07.
- Recomeço da série após as 4 partidas — fora do v1 (Q3 do grill da 05).
- Autenticação, TLS, token, segunda mesa e escolha manual de assento — fora do v1 (`docs/adr/0002`, `docs/adr/0005`).
- Modo imagem com os PNGs — ADR 0004; `PATH_IMAGENS` e as constantes de imagem do esqueleto saem com ele (decisão 15).
- Re-ligar o dark/light e listar as teclas no `Footer` — sprint 07 (decisão 15); `d` e `action_toggle_dark` saem na 06.
- Um widget ou biblioteca de UI além do Textual, arquivo `.tcss` próprio e tema — ADR 0004 e o teto de `80x24`.
- Reusar o `Servidor` real ou os robôs de `tests/test_servidor.py` como servidor de teste — o teste usa um falso roteirizado (decisão 8).
- Fazer o cliente sobreviver a um servidor hostil (limite de leitura folgado, reconexão automática): fora do v1; a falha vira aviso de tela (decisão 13).

## Decisões

**1. A leitura do fio é um worker `@work(exclusive=True)` do Textual, no mesmo event loop — não uma thread.**
Critério: o ADR 0001 fecha o modelo dirigido a eventos do ADR 0002, e o Textual já roda o seu próprio loop; `readline()` é `await`, então a UI continua respondendo sem thread nem `call_from_thread`. O worker é o único ponto do cliente que importa `protocolo` e ele **termina** traduzindo a mensagem: a partir daí só chama métodos de estado do `App` (`mostrar_estado`, `avisar`), que é o que a decisão do PLANO exige ("só traduz mensagem em método de tela"). Alternativa rejeitada: thread própria com `asyncio.run` — um segundo loop, uma fila entre loops e `call_from_thread` em cada atualização, tudo para não usar o loop que o Textual já tem. Alternativa rejeitada: `asyncio.create_task` no `on_mount` — equivalente em poder, mas fora do ciclo de vida do Textual (sem cancelamento na saída e sem o modo de teste), o que é exatamente o que `@work` entrega.

**2. Um arquivo só, `main.py`, com o worker dentro do `App`.**
Critério: o PLANO nomeia `main.py` como o cliente, a tela inteira cabe em ~150 linhas e a invariante "nenhum widget conhece o protocolo" é sobre widgets, não sobre arquivos — o worker importa `protocolo`, os widgets não. Alternativa rejeitada: `cliente.py` (conexão + worker) separado de `main.py` (tela) — dois módulos, um `Protocol`/callback entre eles e o mesmo teste, para separar o que o teste de qualquer forma exercita junto. Alternativa rejeitada: um pacote `cliente/` com telas — a 06 tem uma tela e um modal; estrutura de quatro arquivos é da 07, se ela precisar.

**3. O assento do jogador é o índice do seu nome em `assentos`; o protocolo não ganha campo.**
Critério: o servidor recusa `nome_em_uso` (spec 05), então o nome é único na mesa, e `Estado.assentos` (`protocolo.py:47`) já viaja em todo snapshot; `assentos.index(nome)` responde "quem sou eu" sem mudar o fio nem a validação estrita da 04. Alternativa rejeitada: `Estado.assento: int` — mudaria o codec, a validação e os testes da 04/05 para economizar um `index`. Alternativa rejeitada: o cliente guardar o assento que o servidor "atribuiu" — o `entrar` não devolve assento, e uma reconexão pode mudar a posição; derivar do snapshot é sempre atual.

**4. "Cima ou baixo" é um `ModalScreen`; a queda é um painel de aviso, não um modal.**
Critério: a pergunta é bloqueante e tem exatamente duas respostas — nenhuma carta pode ser jogada antes dela (o motor recusa jogar com a mão não preparada), então um modal é o encaixe semântico. A queda é um estado passivo que aparece e some conforme `ausentes`, e o jogador precisa continuar vendo a mesa e a própria mão enquanto espera; um modal teria de ser empilhado e desempilhado a cada transição de `ausentes` (inclusive no meio de um erro), com mais caminhos do que o painel. Alternativa rejeitada: painel para os dois — o cima/baixo perderia o "estou travado nisto" e as teclas de jogada seriam processadas com a mão vazia. Alternativa rejeitada: modal para os dois — modal de queda fica obsoleto quando o dono reconecta e o pop teria de competir com o próximo snapshot. No congelamento o cliente MUST NOT bloquear as teclas: quem recusa a jogada é o servidor (`mesa_congelada`), como já faz com a vez (decisão 12 da 05) — um "pode jogar agora" local seria a segunda verdade que a sprint 02 proibiu.

**5. Cartas em texto com markup do Textual, a mão em uma linha, copas e ouros em vermelho.**
Critério: é literalmente o ADR 0004 (`A♥`, `7♠`, copas/ouros coloridos) e a mitigação do risco de `80x24` do PLANO: dez cartas de dois caracteres mais separador ficam em ~30 colunas, dentro de 80; a mão ocupa uma linha fixa e a vaza cabe no painel da mesa com o nome do assento ao lado da carta. Os símbolos são `♣ ♥ ♠ ♦` (os quatro naipes do ADR 0004), e o realce da seleção usa o markup de `reverse`/`bold` — cor de naipe e destaque são o mesmo sistema de markup, não dois. Alternativa rejeitada: `ListView`/`DataTable` de cartas — mais widgets e foco, e a mão continua tendo de caber em uma linha; alternativa rejeitada: `textual-image` com os PNGs — dependência nova, proibida pelo ADR 0004; alternativa rejeitada: desenhar a carta em `rich.Text` montado à mão — reintroduz o que o markup do `Static` já faz.

**6. A seleção é um índice inteiro com três `Binding`s, não um widget de lista.**
Critério: a mão tem dez cartas que são substituídas a cada snapshot e a única operação é mover/confirmar; um inteiro com `clamp` e `Enter` é menos código do que instanciar e repopular uma lista focável, e o teste pilota com `pilot.press("left"/"right"/"enter")` sem lidar com foco. Alternativa rejeitada: `OptionList` — traria foco, `OptionSelected` e um segundo sistema de destaque, e ainda pediria um `Binding` de `Enter` próprio. Alternativa rejeitada: teclas numéricas por carta — mais teclas para o jogador decorar e não cobre o "destacar" pedido no entregável.

**7. A tela é uma função do snapshot: um `#aviso` com prioridade, não um roteador de `Screen`s.**
Critério: o estado inteiro chega a cada evento (ADR 0002), então a tela é `f(Estado)`; a ordem das fases é explícita e testável — `ausentes` > `trunfo is None` com `respondente == meu_assento` (diálogo) > `trunfo is None` (espera `N de 4`) > mesa em jogo. Alternativa rejeitada: `push_screen`/`switch_screen` por fase — quatro telas para um layout que só troca o miolo, e o teste teria de perseguir a pilha de telas em vez de ler o painel. O `ModalScreen` do cima/baixo é a exceção porque é bloqueante (decisão 4).

**8. O teste usa um servidor falso roteirizado (`asyncio.start_server` que fala o protocolo de verdade), não o `Servidor` nem um mock de socket.**
Critério: o PLANO pede "um servidor falso", e a tela precisa de estados exatos (dois de quatro, respondente em mim, `ausentes == [2]`) que o `Servidor` real só alcança com uma série determinística de mãos; o falso manda o `Estado` exato e **grava** as intenções do cliente, então cada cenário é um `enviar` e um `assert`. Como o falso usa `serializar`/`desserializar` do `protocolo.py:95,162`, o teste continua exercitando o codec real dos dois lados. Alternativa rejeitada: o `Servidor` real — acoplaria o teste da tela às regras do motor e ao `random`, e o cenário "caído" exigiria cortar uma conexão no meio de uma mão. Alternativa rejeitada: `unittest.mock` em `open_connection` — o teste nunca veria bytes, e o bug de serialização do cliente passaria. Alternativa rejeitada: `pytest-asyncio` + fixtures — dependência nova (ADR 0004) para marcar testes que já sabem rodar sob `asyncio.run`.

**9. Leitura determinística no teste: `asyncio.Queue` e `wait_for`, sem `sleep`.**
Critério: é a lição da 05 ("teste de servidor precisa de leitura determinística") — o falso notifica cada mensagem recebida numa fila, e o teste faz `await asyncio.wait_for(fila.get(), 1)`; a tela é atualizada com `await pilot.pause()`. Nada no teste espera o relógio andar nem drena até timeout. Alternativa rejeitada: `sleep` curto entre o `press` e o `assert` — flaky no CI. Alternativa rejeitada: ler a fila do cliente — o teste assere a tela (o que o jogador vê), não os widgets internos do `App`.

**10. O cliente também fecha a conexão quando o leitor estoura o limite; EOF, reset, teto e `OSError` convergem no mesmo caminho.**
Critério: a lição da 05 vale do outro lado do fio — todo caminho de leitura de socket termina no mesmo `finally`, sem exceção escapando para o loop (o `ValueError` do `readline` acima do `limit` é o caso que escapou lá). O cliente abre com um `limit` folgado (o snapshot legítimo é < 1 KB) e trata o estouro como fim de conexão; `desserializar` continua sendo o único validador de forma. Alternativa rejeitada: `limit=TETO_LINHA` no cliente — o teto é defesa do **servidor** contra cliente hostil (ADR 0002/04); replicá-lo no cliente não protege ninguém e transformaria o limite em contrato dos dois lados sem um teste que o peça.

**11. Dois scripts no `pyproject.toml`: `pysueca` (cliente) e `pysueca-servidor` (servidor), com `argparse` e defaults `127.0.0.1:8765`.**
Critério: são dois processos com ciclos de vida distintos, e o roteiro de 4 terminais precisa dos dois; `argparse` é stdlib e `main(argv)` é testável sem subir socket (o `argv` vira `Namespace` e o comando é montado a partir dele). Alternativa rejeitada: um script com subcomando (`pysueca servidor`) — um subparser e um ramo de despacho para economizar uma linha de `[project.scripts]`. Alternativa rejeitada: só o cliente, com o servidor por `python -m pysueca.servidor` — o `python -m` funciona, mas o roteiro ficaria com dois estilos de comando, e o PLANO nomeia o entrypoint quebrado como entregável. `127.0.0.1` é o default; o bind para duas máquinas é a 07.

**12. A tradução dos motivos de `erro` para linguagem de jogador e o placar final ficam para a 07; a 06 mostra o motivo cru e o que o snapshot traz.**
Critério: o entregável da 07 nomeia "mensagens de erro do servidor visíveis na tela" e "placar final do jogo" — se a 06 já traduzisse, a 07 não teria o que fazer e a divisão do PLANO se perderia. A 06 precisa apenas não perder a mensagem (o jogador e o verificador leem `nome_em_uso` no painel). Alternativa rejeitada: tabela de tradução já na 06 — antecipa o escopo da 07 sem teste que a peça. Alternativa rejeitada: engolir o `erro` — aí a recusa some da tela e o jogador fica sem saber por que a jogada não andou.

**13. Sem `asyncio.Lock` e sem fila de saída: o cliente escreve direto no `StreamWriter` de dentro das ações de tela.**
Critério: o worker e as ações rodam no mesmo loop, e `write` + `await drain` não intercalam com o `readline` (o `drain` pode suspender, mas não muta estado compartilhado). Um `lock` protegeria uma corrida que não existe, como na 05 (decisão 3 de lá). Alternativa rejeitada: fila de saída consumida pelo worker — o worker está bloqueado no `readline`, então a fila pediria uma segunda task só para drenar. Alternativa rejeitada: `create_task(drain)` por mensagem — cria uma task por tecla para não esperar um buffer de ~100 bytes.

**14. `#aviso` acumula queda, conexão e erro com prioridade explícita; a mesa em jogo é o resto do layout.**
Critério: um único painel com ordem documentada (`ausentes` > "sua vez"/"vez de X" > "conectando") é o que o teste lê e o que a 07 vai polir; separar os avisos em widgets piores não muda a informação. O aviso de `erro` fica até o próximo snapshot — aceito, porque o próximo evento é a mesa andando e a 07 vai dar tempo de leitura à mensagem. Alternativa rejeitada: notificação do Textual (`self.notify`) — some sozinha no relógio e o teste ficaria dependente do timer de notificação.

**15. O esqueleto do `main.py` sai inteiro: `PATH_IMAGENS`, `NAIPES`, `CARTAS`, o binding `d` e `action_toggle_dark`.**
Critério: nada disso tem consumidor (as constantes de `main.py:19-39` são de um modo imagem sem pasta e com nomes em inglês) e o PLANO nomeia "`d` relica o dark/light existente" como entregável da 07, junto das teclas no `Footer` — manter o binding agora antecipa um item da 07 e deixa de pé o único erro do `mypy src` (`main.py:52`), que a 10.2 fecha. Alternativa rejeitada: manter o `d` e consertar a tipagem agora — um `cast`/`# type: ignore` para uma tecla que a 07 vai reescrever.

**16. A tela consome todos os campos públicos do snapshot: `contagens` no `#assentos` e `carta_trunfo` no `#mesa`.**
Critério: a 04 desenhou o snapshot para a tela — `contagens` existe porque o assento vê a própria mão e apenas a contagem das outras, e `carta_trunfo` é público porque a carta fica virada na mesa; `Nome 10` ao lado de cada assento e a carta `A♥` no painel da mesa fecham o ciclo do campo até a ponta, sem tela nova. Alternativa rejeitada: mostrar só o naipe do trunfo — `carta_trunfo` ficaria sem consumidor na TUI. Alternativa rejeitada: omitir as contagens — a informação existe no snapshot e a vaza corrente mostra a diferença (quem já jogou tem uma carta a menos).

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| `80x24` apertado para 4 assentos + 10 cartas (risco nomeado no PLANO) | mão em uma linha (~30 colunas) com o realce dentro do markup, e o painel da mesa em uma linha por vaza: `Ana: 7♥  Bia: A♣` |
| Tooltip/notificação/modal competindo com o worker por foco | a tela é função do snapshot (decisão 7); o único modal é o cima/baixo, empilhado só sob a condição `respondente == meu_assento` e desempilhado no snapshot preparado |
| O teste da tela ficar flaky sob `run_test` | leitura determinística por `asyncio.Queue` (decisão 9), sem `sleep`; `pilot.pause()` depois de cada `enviar`; o timeout de `wait_for` é asserção, não espera |
| O worker morrer em silêncio e a tela congelar | o `finally` único do worker (decisão 10) sempre passa por um aviso de conexão; o teste "sem servidor o cliente avisa" cobre o caminho mais comum (porta fechada) |
| Um widget começar a importar `protocolo` ("só um camposinho") | a invariante vira teste de fronteira: o teste assere a tela pelo texto renderizado, nunca o tipo `Estado`, e o `AGENTS.md` registra a regra (task de documentação) |
| A reescrita do `main.py` derrubar a cobertura do pacote | `--cov-fail-under=80` já é o gate do `AGENTS.md` desde a 04; `test_cliente.py` cobre o `main.py` novo e o `main()` novo do `servidor.py` |
| O entrypoint novo não ser exercitado por teste | `main(argv)` recebe `argv` e devolve/monta o `Namespace`; o teste cobre nome/host/porta/defaults e o caso de argumento desconhecido sem subir socket (decisão 11) |
| `mypy` vermelho no `App.dark` sobreviver à reescrita | o `mypy src` é task de validação final; se o `App.dark` continuar reclamando, o `toggle_dark` sai (a 07 decide as teclas do `Footer`) |
| O servidor falso divergir do protocolo real | o falso serializa e desserializa com `protocolo.py` (decisão 8) — não há segundo codec; a integração real continua provada por `tests/test_servidor.py` |

## Plano de Migração

Reescrita de `src/pysueca/main.py` (esqueleto de 57 linhas → cliente), adição de `tests/test_cliente.py`, duas linhas no `pyproject.toml` e `main()` no `servidor.py`. Nenhuma API existente muda: `carta.py`, `baralho.py`, `motor.py`, `protocolo.py` e o `Servidor` ficam intactos, e `tests/test_servidor.py` roda sem alteração. Rollback: `git checkout main.py`, apagar `tests/test_cliente.py`, reverter as duas linhas do `pyproject.toml` e o `main()` do `servidor.py` — nada do jogo depende do cliente. Nenhuma dependência nova (`docs/adr/0004`); nenhuma migração de dados.

## Questões Abertas

Nenhuma — as pendências fecharam no grill:

- **Cima ou baixo e queda: modal ou painel?** Modal para o cima/baixo e painel `#aviso` para a queda (decisão 4); nenhum bloqueio local das teclas no congelamento — o servidor recusa com `mesa_congelada`.
- **Nome do jogador: posicional ou `--nome`?** Posicional obrigatório (`pysueca Ana`): qualquer default colidiria no quarto terminal da mesma máquina (`nome_em_uso`), e o erro só apareceria depois de subir a tela.
- **Dois entrypoints ou subcomando?** Dois (`pysueca` e `pysueca-servidor`), decisão 11.
- **Roteiro do `README.md`: teste de documentação ou leitura?** Leitura manual (10.5) — nenhum teste vigiando prosa que a 07 reescreve; o cenário fica na spec como NÃO TESTÁVEL.
- **`erro` no `#aviso`: até o próximo snapshot ou no relógio?** Até o próximo snapshot (decisão 14), sem `notify` e sem timer no teste.
- **O `toggle_dark` do esqueleto sobrevive?** Não (decisão 15); a 07 re-liga o dark/light com as teclas no `Footer`.
- **Contagens de cartas e carta do trunfo na tela?** As duas (decisão 16), em `#assentos` e `#mesa`.

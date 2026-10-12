# Design — Sprint 04 — Protocolo

> **Sprint:** `sprints/04-protocolo/` — decisão do PLANO: uma linha JSON por mensagem, com snapshot `estado` completo a cada evento (ADR 0002) e validação estrita no `protocolo.py`, usada pelos dois lados; o teto de bytes por linha é o único caso fatal, o resto é `erro` recuperável; o nome é normalizado (`strip`, 1 a 20 caracteres) antes de virar identidade.
> **Depende de:** Sprint 03 — Jogo e papéis (concluída)

## Contexto

O motor está completo e provado: `Carta`/`Naipe`/`Valor` (`carta.py`), `Baralho` (`baralho.py`), `Vaza`/`Mao`/`ErroJogada`/`Resultado` e `Jogo` (`motor.py:141`, 99% de cobertura). O ADR 0002 fixou o transporte — TCP cru, uma linha JSON por mensagem, snapshot completo por destinatário — e o ADR 0004 fixou stdlib pura. Não existe `protocolo.py`: o formato de fio, a validação da linha e o snapshot não têm dono. A sprint 02 já fixou a fronteira (decisão 3): erros de regra (vez, posse, naipe) no motor; erros de fio (tipo, campo, tamanho, nome) no protocolo, que apenas formata o `ErroJogada` recebido.

Esta sprint cria `src/pysueca/protocolo.py`, puro e sem rede, e `tests/test_protocolo.py`.

## Objetivos / Não objetivos

**Objetivos:**
- `src/pysueca/protocolo.py`: as cinco mensagens (`entrar`, `responder`, `jogar`, `estado`, `erro`), `serializar`/`desserializar` de uma linha JSON, o teto de bytes, a validação estrita recuperável, o snapshot por assento e a formatação do `ErroJogada`.
- `tests/test_protocolo.py` verde, provando a ida-e-volta, o mascaramento do snapshot, as recusas recuperáveis e o teto fatal — sem `asyncio`, socket ou Textual.
- Reusar `Carta.texto`/`de_texto` (sprint 01), `ErroJogada` (sprint 02) e o estado do `Jogo` (sprint 03) como estão.

**Não objetivos:**
- Socket, `asyncio`, `start_server`, reconexão e congelamento da mesa — sprint 05. Aqui o teto só **sinaliza** a violação; quem fecha a conexão é o servidor.
- Tela, cartas coloridas e teclas — sprint 06.
- Mensagem de `puxar` separada: a sprint 02 fundiu puxar e seguir em `Mao.jogar`; o fio tem só `jogar`.
- Erros de assento/conexão (`nome_em_uso`, `não sentado`) — dono é o servidor (05).
- Autenticação, TLS e versionamento de protocolo — fora do v1 (`docs/adr/0002`).

## Decisões

**1. `protocolo.py` é puro: texto entra, texto sai; nada de socket, `asyncio` ou Textual.**
Critério: é a decisão do PLANO ("serializar e desserializar sem nenhuma rede") e a invariante do `AGENTS.md` (motor puro e síncrono; só a 05 é casca `asyncio`). O protocolo é testável sem rede, e o teto de bytes vira uma função pura que a 05 chama ao ler o socket. Alternativa rejeitada: embutir o `readuntil`/`StreamReader` no protocolo — acoplaria o formato à rede e repetiria o teste de socket em todo cenário de fio.

**2. Uma dataclass por mensagem; `serializar`/`desserializar` são as duas únicas funções que tocam JSON.**
Critério: o servidor (05) e a TUI (06) leem campos por atributo (`msg.carta`, `msg.nome`), não por `msg["carta"]`; o `mypy` cobre os dois lados e o JSON fica confinado num módulo. Alternativa rejeitada: `dict` cru — espalha `["tipo"]` e chaves mágicas por 05/06, sem tipo e sem um único lugar para validar. Alternativa rejeitada: hierarquia com classe-base `Mensagem` e `match` no `tipo` — a união de cinco dataclasses não precisa de `isinstance` se o `tipo` é o discriminador do JSON; a classe-base só acrescentaria cerimônia.

**3. `desserializar` devolve `Erro` para a recusa recuperável e levanta `LinhaLonga` só no teto.**
Critério: o PLANO diz que só a violação de tamanho é fatal e o resto é `erro` recuperável; a assinatura `Mensagem | Erro` torna o caminho recuperável explícito (o servidor reenvia o `Erro` sem `try/except` por linha), enquanto a exceção única marca o caso que fecha a conexão. Alternativa rejeitada: levantar `ErroProtocolo` para tudo — obrigaria o servidor a capturar exceção a cada linha só para não morrer, e apagaria a diferença entre "responder erro e seguir" e "fechar".

**4. O teto é `TETO_LINHA = 4096` bytes UTF-8, contando o `\n`.**
Critério: o ADR 0002 recusou deltas justamente porque o snapshot inteiro é barato, e o maior snapshot legítimo (10 cartas + 4 assentos + placar) fica abaixo de 1 KB; 4096 dá folga e corta o ataque de memória. O `\n` entra na conta porque é o que o `readline` com limite vai medir. O teto é aplicado **só na desserialização (leitura)**, a ponta que vem de fora; `serializar` não precisa do guard, porque o servidor é a fonte da mensagem, não o atacante. Alternativa rejeitada: teto por caractere — um nome ou texto multibyte contaria a menos que os bytes lidos; a defesa é sobre bytes.

**5. O nome é normalizado no protocolo, não no servidor.**
Critério: o PLANO põe o `strip` e o limite de 1–20 no `protocolo.py`, e a identidade do ADR 0005 é o nome — com a normalização no codec, "Ana" e " Ana " são o mesmo assento nos dois lados, e nenhum servidor pode esquecer de normalizar. Alternativa rejeitada: normalizar no `Entrar` do servidor — a regra ficaria a um `if` de distância do bug de dois assentos com o mesmo nome.

**6. A carta viaja como `"7H"`; o naipe como `"C"/"H"/"S"/"D"`; `responder.cima` é booleano.**
Critério: `Carta.texto`/`de_texto` (`carta.py:71,75`) já são ida-e-volta provados na sprint 01 — o protocolo não inventa um segundo formato. `cima: true/false` espelha `Mao.preparar(cima: bool)`; a TUI só decide qual dos dois botões manda. Alternativa rejeitada: `"resposta": "cima"|"baixo"` — criaria uma tradução string→bool em algum lugar, sem ganho. JSON é UTF-8 e uma linha por mensagem (ADR 0002).

**7. `estado(jogo, nomes, assento) -> Estado` monta o snapshot; o mascaramento é do protocolo.**
Critério: a regra "própria mão inteira, alheias só como contagem" é do fio (ADR 0001: o cliente recebe apenas a própria mão) e precisa de um dono único — se o servidor montasse o dicionário, o vazamento de mão dependeria da disciplina de 05. O protocolo recebe o `Jogo` e a lista de nomes por assento (`str | None`), que é o único dado de assento que ele precisa; quem guarda os nomes e a ocupação é o servidor. Alternativa rejeitada: o protocolo só definir a dataclass e o servidor preencher — o teste de mascaramento da 04 não teria o que exercitar e a regra ficaria sem dono.

Campos do `Estado` (os "não ditos" ficam nas Questões Abertas):
`assentos: list[str | None]` (4, nome ou vazio), `mao: list[str]` (só do destinatário), `contagens: list[int]` (4), `trunfo: str | None`, `carta_trunfo: str | None`, `vez: int | None`, `respondente: int | None` (quem deve responder "cima ou baixo"; `None` sem pergunta pendente), `vaza: list[tuple[int, str]]`, `partidas: list[int]` (2), `encerrado: bool`, `vencedor: int | None`.

**8. `erro_de_jogada(ErroJogada) -> Erro` só formata; nenhuma regra no protocolo.**
Critério: fecha a fronteira da sprint 02 (decisão 3) — o motor decide o erro, o protocolo dá o identificador de fio. Os três motivos (`fora_da_vez`, `carta_fora_da_mao`, `nao_seguiu_naipe`) são os `ErroJogada` existentes (`motor.py:16-18`), sem enum novo. Alternativa rejeitada: o protocolo revalidar vez/posse/naipe para "ajudar" — duplicaria a regra e criaria duas verdades.

**9. O `erro` carrega `motivo` (identificador estável), não texto humano; e campo extra é recusado.**
Critério: o cliente é nosso e a tela (07) escolhe o texto; um `detalhe` humano no fio seria a mesma string em três lugares. Os motivos de fio são `json_invalido`, `tipo_desconhecido`, `campo_faltando`, `campo_extra` e `nome_invalido`; os de jogada vêm de `erro_de_jogada`. A validação estrita recusa o campo que o protocolo não conhece (`campo_extra`), porque os dois lados saem do mesmo repositório e da mesma versão — campo extra é digitação, não compatibilidade futura. Alternativa rejeitada: mensagem pronta no servidor — engessa o texto e mistura apresentação com transporte. Alternativa rejeitada: ignorar campos extras — engoliria o typo do cliente em silêncio.

**10. O codec fala `bytes`, não `str`.**
`serializar` devolve a linha UTF-8 terminada em `\n`; `desserializar` aceita os bytes lidos, e a fatal é a exceção `LinhaLonga`. Critério: o teto é contado em bytes e o socket da 05 é `StreamReader`/`StreamWriter` (`bytes`) — o casamento é direto, sem codificar/decodificar a cada linha. Alternativa rejeitada: `str` — a 05 decodificaria toda linha e o teto passaria a contar caracteres, não bytes. Alternativa rejeitada: sentinela no retorno em vez de exceção — o `match` da 05 ganharia um ramo e um tipo próprio só para o caso fatal.

**11. O `Estado` não carrega a fase da mesa e tolera a mão não preparada.**
Critério: "espera" (faltam jogadores) e "congelada" (conexão caída) são estado de conexão/assento — dono é a 05, não o `Jogo`; a 04 não inventa estado de servidor. Depois de `encerrar_mao`, o `Jogo` cria uma `Mao` não preparada (`motor.py:165`) que ainda não tem `trunfo`/`carta_trunfo`; o snapshot devolve `None` nesses campos e `contagens` zeradas, e o cliente (06) lê isso como "mão ainda não começou". Alternativa rejeitada: `fase: "espera"|"jogo"|"fim"` — "espera" e "congelada" não seriam representáveis sem trazer o modelo de conexão para a 04.

## Riscos / Compensações

| Risco | Mitigação |
|---|---|
| O snapshot vaza a mão de outro assento | `estado()` é o único construtor do campo `mao`, e o teste varre a linha serializada inteira procurando as cartas alheias, não só o campo `mao` |
| Teto apertado demais corta um snapshot legítimo | 4096 bytes com folga sobre um snapshot de < 1 KB; EDGE de linha exatamente no limite prova a fronteira |
| O protocolo virar um segundo dono da regra de jogo | `erro_de_jogada` só traduz o enum do motor; nenhum `if` de vez/posse/naipe na sprint — teste de fronteira explicitamente verde sem código novo |
| Validação estrita travar a evolução do formato entre 04 e 06 | os dois lados saem do mesmo repositório e da mesma versão; campo novo entra com spec própria e campo extra é recusado (decisão 9) |
| JSON aceitar tipo errado (`"carta": 7`, `"cima": "sim"`) | a validação de shape checa tipo de cada campo obrigatório, não só presença; cenário de campo faltando cobre o caminho |
| `desserializar` engolir erro e devolver `Erro` onde o chamador esperava exceção | assinatura explícita `Mensagem | Erro`; só `LinhaLonga` é exceção, e o EDGE "nenhum outro erro é fatal" ancora |

## Plano de Migração

N/A — código aditivo (um módulo e um teste novos). Nenhuma API existente muda; `carta.py`, `baralho.py` e `motor.py` ficam intactos. Rollback é apagar `src/pysueca/protocolo.py` e `tests/test_protocolo.py`. Nenhuma dependência nova (`docs/adr/0004`).

## Questões Abertas

Nenhuma — as pendências fecharam no grill:

- Campos extras desconhecidos são **recusados** com motivo `campo_extra` (decisão 9).
- `Estado.respondente: int | None` entra nesta sprint: quem deve responder "cima ou baixo", `None` sem pergunta pendente (decisão 7).
- O `erro` carrega só `motivo`; sem `detalhe` humano (decisão 9).
- `TETO_LINHA = 4096`, aplicado só na leitura (decisão 4).
- Sem `fase` no `Estado`; a fase da mesa e o `congelada` ficam para a 05 (decisão 11).
- O codec fala `bytes` (UTF-8 com `\n`) e a fatal é a exceção `LinhaLonga` (decisão 10).

# QA Plan — Sprint 04 — Protocolo

> **Sprint:** `sprints/04-protocolo/` — rastreia `sprints/04-protocolo/specs/<capability>/spec.md`

## Capability: protocolo

### Test: entrar faz ida-e-volta
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio — CRITICAL
- **GIVEN** uma mensagem `Entrar` com o nome `"Ana"`
- **WHEN** `serializar` gera a linha e `desserializar` a lê de volta
- **THEN** a mensagem devolvida é `Entrar("Ana")`, com o tipo `entrar` preservado

### Test: responder faz ida-e-volta
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio
- **GIVEN** as mensagens `Responder(cima=True)` e `Responder(cima=False)`
- **WHEN** cada uma é serializada e desserializada
- **THEN** volta a mesma mensagem, com o mesmo valor de `cima`

### Test: jogar faz ida-e-volta
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio — CRITICAL
- **GIVEN** uma mensagem `Jogar` com a carta `Carta(Naipe.COPAS, Valor.SETE)` (`"7H"`)
- **WHEN** é serializada e desserializada
- **THEN** o campo `carta` viaja como `"7H"` e volta `Carta(COPAS, SETE)`

### Test: estado faz ida-e-volta
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio
- **GIVEN** um snapshot `Estado` montado de um `Jogo` real (assentos, mão, contagens, trunfo, vaza, placar e `respondente`)
- **WHEN** é serializado e desserializado
- **THEN** volta um `Estado` igual ao original, com todos os campos preservados

### Test: erro faz ida-e-volta
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Mensagens de fio — CRITICAL
- **GIVEN** um `Erro` vindo de `erro_de_jogada(ErroJogada.FORA_DA_VEZ)`
- **WHEN** é serializado e desserializado
- **THEN** volta `Erro("fora_da_vez")`

### Test: EDGE - linha malformada vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — EDGE
- **GIVEN** as linhas `"{"`, `"não é json"` e `"[1, 2]"` (JSON que não é objeto)
- **WHEN** `desserializar` as lê
- **THEN** devolve `Erro` com motivo `json_invalido`, sem levantar exceção

### Test: EDGE - tipo desconhecido vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — EDGE
- **GIVEN** a linha `{"tipo": "assobiar"}`
- **WHEN** `desserializar` a lê
- **THEN** devolve `Erro` com motivo `tipo_desconhecido`

### Test: EDGE - campo faltando vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — EDGE
- **GIVEN** as linhas `{"tipo": "jogar"}` (sem `carta`), `{"tipo": "entrar"}` (sem `nome`) e `{"tipo": "responder"}` (sem `cima`)
- **WHEN** `desserializar` as lê
- **THEN** devolve `Erro` com motivo `campo_faltando` para cada um

### Test: EDGE - campo extra vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — EDGE
- **GIVEN** a linha `{"tipo": "jogar", "carta": "7H", "cor": "azul"}`
- **WHEN** `desserializar` a lê
- **THEN** devolve `Erro` com motivo `campo_extra`

### Test: EDGE - campo com tipo errado vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — EDGE
- **GIVEN** a linha `{"tipo": "jogar", "carta": 7}`
- **WHEN** `desserializar` a lê
- **THEN** devolve `Erro` com motivo `campo_invalido`

### Test: nome é normalizado
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — CRITICAL
- **GIVEN** a linha `{"tipo": "entrar", "nome": "  Ana  "}`
- **WHEN** `desserializar` a lê
- **THEN** devolve `Entrar("Ana")`, sem os espaços em volta

### Test: EDGE - nome inválido vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Validação estrita recuperável — EDGE
- **GIVEN** um `entrar` com nome `"   "` (vazio após `strip`) e um com 21 caracteres
- **WHEN** `desserializar` os lê
- **THEN** devolve `Erro` com motivo `nome_invalido` para cada um

### Test: EDGE - linha acima do teto é fatal
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Teto de bytes por linha — EDGE
- **GIVEN** uma linha com `TETO_LINHA + 1` bytes UTF-8
- **WHEN** `desserializar` a lê
- **THEN** levanta `LinhaLonga` — o único caso fatal, que o servidor (05) traduz em fechar a conexão

### Test: EDGE - linha no limite é aceita
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Teto de bytes por linha — EDGE
- **GIVEN** uma linha `entrar` com exatamente `TETO_LINHA` bytes (nome no limite de 20)
- **WHEN** `desserializar` a lê
- **THEN** é aceita, sem violação de tamanho

### Test: EDGE - nenhum outro erro é fatal
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Teto de bytes por linha — EDGE
- **GIVEN** linha malformada, tipo desconhecido, campo faltando e campo extra, todas pequenas
- **WHEN** `desserializar` as lê
- **THEN** nenhuma levanta `LinhaLonga`; todas devolvem `Erro` recuperável

### Test: snapshot traz a própria mão
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento — CRITICAL
- **GIVEN** um `Jogo` com a mão preparada (`random.Random` determinístico) e o assento 2 como destinatário
- **WHEN** `estado(jogo, nomes, assento=2)` monta o snapshot
- **THEN** o campo `mao` traz exatamente as 10 cartas de `jogo.mao.maos[2]`

### Test: EDGE - snapshot traz só a contagem das outras mãos
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento — CRITICAL
- **GIVEN** o mesmo snapshot do assento 2, serializado
- **WHEN** a linha inteira é procurada pelas cartas dos assentos 0, 1 e 3
- **THEN** nenhuma carta alheia aparece em campo algum, e `contagens` é `[10, 10, 10, 10]`

### Test: EDGE - snapshot reflete a mesa
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento — EDGE
- **GIVEN** um `Jogo` com carta do trunfo virada, uma vaza em andamento e placar `[2, 0]`
- **WHEN** `estado(...)` monta o snapshot
- **THEN** traz `trunfo`, `carta_trunfo`, `vez`, a `vaza` corrente com assento e carta, `partidas == [2, 0]` e `encerrado is False`

### Test: snapshot diz quem deve responder
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Snapshot por assento — CRITICAL
- **GIVEN** um `Jogo` com a pergunta "cima ou baixo" pendente (mão ainda não preparada)
- **WHEN** `estado(...)` monta o snapshot
- **THEN** `respondente` é `(embaralhador + 1) % 4`; com a mão já preparada, `respondente` é `None`

### Test: EDGE - jogada fora da vez vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Erro de jogada formatado — EDGE
- **GIVEN** um `Jogo` preparado cuja vez é do assento 0
- **WHEN** o assento 2 tenta jogar e o motor devolve `ErroJogada.FORA_DA_VEZ`
- **THEN** `erro_de_jogada` devolve um `Erro` com motivo `fora_da_vez`

### Test: EDGE - carta fora da mão vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Erro de jogada formatado — EDGE
- **GIVEN** o assento da vez tentando jogar uma carta que está com outro assento
- **WHEN** o motor devolve `ErroJogada.CARTA_FORA_DA_MAO`
- **THEN** `erro_de_jogada` devolve um `Erro` com motivo `carta_fora_da_mao`

### Test: EDGE - não seguir o naipe vira erro
**Traces**: `sprints/04-protocolo/specs/protocolo/spec.md` → Requirement: Erro de jogada formatado — EDGE
- **GIVEN** uma vaza com naipe puxado e um assento que tem o naipe e joga outro
- **WHEN** o motor devolve `ErroJogada.NAO_SEGUIU_NAIPE`
- **THEN** `erro_de_jogada` devolve um `Erro` com motivo `nao_seguiu_naipe`

## Casos Limite

- O teto conta **bytes** UTF-8, não caracteres: um nome multibyte no limite muda a conta; a linha inclui o `\n`.
- `linha no limite` prova a fronteira fechada (`len(linha) == TETO_LINHA` aceita, `+ 1` fatal).
- JSON que não é objeto (`[1, 2]`, `42`, `"texto"`) é recusa, não crash.
- Campo com o tipo errado (`"carta": 7`, `"cima": "sim"`, `"nome": 42`) vira `campo_invalido` (não `campo_faltando`), e é recusa, não crash — a validação checa tipo, não só presença.
- Campo extra é recusa (`campo_extra`), distinta de campo faltando (`campo_faltando`): a validação compara o conjunto exato de chaves.
- As cartas alheias não podem aparecer **em campo algum** da linha serializada, não só no campo `mao` (o teste varre a string inteira).
- Nome no limite de 20 caracteres é aceito; 21 é recusado; espaços em volta não contam para o limite.
- `desserializar` não engole a exceção fatal: `LinhaLonga` é o único `raise`, e todo o resto volta como `Erro`.

## Pontos de Integração

- `serializar`/`desserializar` usam `Carta.texto`/`de_texto` (`carta.py:71,75`) — um só formato de carta no projeto.
- `erro_de_jogada` traduz os três `ErroJogada` (`motor.py:16-18`); nenhum `if` de vez/posse/naipe no protocolo (fronteira da sprint 02, decisão 3).
- `estado(jogo, nomes, assento)` lê `Jogo.mao`/`partidas`/`encerrado`/`vencedor` (`motor.py:141`) sem mutar o motor.
- `serializar`/`desserializar` serão chamados pelo servidor (05) e pela TUI (06); a 05 é quem traduz `LinhaLonga` em fechar a conexão.
- `pyproject.toml` não muda: nenhuma dependência nova (`docs/adr/0004`).

## Notas de Revisão

- **Dois recursos de exceção convivendo:** `Erro` (devolvido) e `LinhaLonga` (levantada) são intencionais — o PLANO define que só a violação de tamanho é fatal. O EDGE "nenhum outro erro é fatal" ancora a distinção.
- **Cobertura, não RED:** os três testes de `erro_de_jogada` compartilham a mesma função de uma linha (mapa `ErroJogada → motivo`); o primeiro fica RED e os outros dois provam o mapa com entradas diferentes. O EDGE "snapshot reflete a mesa" cobre os campos que o RED de "própria mão" já introduz — registrar como cobertura, não inflar a implementação para forçar vermelho (lição das sprints 01–03).
- **Mascaramento é requisito de segurança do fio:** o teste procura as cartas alheias na **linha serializada inteira**, não só no campo `mao` — um vazamento em `vaza`, `contagens` ou qualquer campo novo falha o teste.
- **Resolvido no grill:** campo extra recusado com motivo `campo_extra`; `Estado.respondente` entra nesta sprint; o `erro` carrega só `motivo` (sem `detalhe` humano); `TETO_LINHA = 4096` aplicado só na leitura. Nada ficou pendente para `pi-atualizar`.
- **Retrabalho da verificação (2026-10-12):** `erro faz ida-e-volta` e `EDGE - campo com tipo errado vira erro` fecham as 3 linhas que o `execucao/04-protocolo/relatorio-verificacao.md` deixou descobertas; `campo_invalido` nasce aqui e a decisão 9 do `design.md` acompanha.
- **Cobertura dos testes novos:** `campo extra vira erro` e `snapshot diz quem deve responder` ancoram decisões que não existiam na primeira proposta; se algum falhar, a decisão do grill não chegou ao código.
- **Fixtures reais:** o snapshot usa um `Jogo` real com `random.Random(seed)`, não um dicionário montado à mão — o mesmo padrão das sprints 02/03 (`Mao` de placar forçado só no teste).

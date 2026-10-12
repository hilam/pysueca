# Spec — Capability `avisos`

> **Sprint:** `sprints/07-polimento/` — capability `avisos` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Motivo de recusa em frase de jogador
O cliente SHALL apresentar todo `erro` do fio como uma frase em português de jogador e MUST NOT exibir o código do protocolo na tela. A tradução SHALL morar no cliente — o único processo que fala com o humano — e MUST NOT alterar `protocolo.py`, que segue com código estável no fio. Um motivo não previsto pelo dicionário SHALL cair numa frase genérica e MUST NOT derrubar o app nem vazar o código cru. A tradução SHALL cobrir todos os códigos de motivo do v1 — os do motor, os do servidor e os da forma do fio — de modo que o fallback só apareça para um motivo novo. Motivos de estado SHALL ser fraseados pela ação recusada (o `mesa_congelada` fala da jogada recusada), para a frase conviver com o aviso de queda no mesmo painel sem repeti-lo. Os avisos que o próprio cliente produz (`Sem conexão`, `Conexão encerrada`) já são frases e SHALL passar intactos.

#### Scenario: a jogada recusada vira frase de jogador
- **WHEN** o servidor manda `erro` com `nao_seguiu_naipe`
- **THEN** o `#aviso` mostra a frase de que é preciso seguir o naipe puxado, sem o código `nao_seguiu_naipe`

#### Scenario: a mesa cheia e o nome em uso viram frase de jogador
- **WHEN** o servidor manda `erro` com `mesa_cheia` ou `nome_em_uso`
- **THEN** o `#aviso` mostra a frase correspondente em português, sem o código do fio

#### Scenario: todos os códigos do v1 têm frase própria
- **WHEN** qualquer código de motivo do v1 (`ErroJogada`, os do servidor e os da forma do fio) passa pela tradução
- **THEN** cada um devolve a sua frase, sem `_` e diferente do código, e nenhum cai no fallback

#### Scenario: EDGE - motivo desconhecido não vaza código nem derruba a tela
- **WHEN** o servidor manda `erro` com um motivo que o dicionário não conhece
- **THEN** o `#aviso` mostra uma frase genérica de recusa, a tela segue de pé e nenhum código de fio aparece

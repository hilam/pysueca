# Spec — Capability `atalhos`

> **Sprint:** `sprints/07-polimento/` — capability `atalhos` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Teclas de jogo visíveis no rodapé
O `Footer` do cliente SHALL mostrar as teclas de jogo — anterior, próxima e jogar — além de `Sair` e do `Tema` (`d`), com a tecla e a descrição de cada `Binding`. O rodapé SHALL continuar mostrando as teclas do diálogo cima ou baixo quando ele estiver aberto. Nenhum `Binding` novo de jogo SHALL ser criado: os três existentes (`left`, `right`, `enter`) deixam de ser ocultos.

#### Scenario: as teclas de jogo aparecem no rodapé
- **WHEN** a tela do cliente monta
- **THEN** o `Footer` mostra a tecla e a descrição de anterior, próxima, jogar e `d`/`Tema`

### Requirement: Tema claro e escuro
`d` SHALL alternar o tema do Textual entre escuro e claro, usando o `action_toggle_dark` da própria biblioteca, sem tema próprio nem CSS novo, e SHALL aparecer no rodapé com a descrição `Tema`. As cores das cartas MUST NOT depender do tema: copas e ouros SHALL continuar vermelhos nos dois temas, porque o markup de naipe é fixo.

#### Scenario: d alterna o tema
- **WHEN** o jogador aperta `d`
- **THEN** o tema do app troca entre escuro e claro, e um segundo `d` volta ao tema anterior

#### Scenario: EDGE - o tema não muda a cor do naipe
- **WHEN** o tema está claro ou escuro
- **THEN** a carta de copas e a de ouros continuam desenhadas em vermelho, sem cor de tema no markup

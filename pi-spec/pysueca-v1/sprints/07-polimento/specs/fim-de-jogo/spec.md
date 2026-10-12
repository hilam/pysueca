# Spec — Capability `fim-de-jogo`

> **Sprint:** `sprints/07-polimento/` — capability `fim-de-jogo` — rastreia `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`

## ADDED Requirements

### Requirement: Fim de jogo na tela
Quando o snapshot trouxer `encerrado` verdadeiro, o cliente SHALL mostrar no painel da mesa o fim do jogo e qual dupla venceu — `vencedor` é o índice da dupla (`0` = assentos 0 e 2, `1` = assentos 1 e 3), e a linha SHALL nomear os dois jogadores da dupla quando os dois nomes existirem em `assentos`, caindo para `dupla 0–2`/`dupla 1–3` quando algum estiver ausente — junto do placar final das partidas. Com a mesa encerrada o cliente MUST NOT anunciar a vez: `vez` continua preenchido no snapshot depois da última vaza, e a tela SHALL ignorá-lo. Com a mesa encerrada a tecla de jogar SHALL NOT enviar `jogar`, para a recusa do servidor (`fora_da_vez`) não aparecer como se a vez fosse de outro; as demais teclas SHALL seguir ativas. O cliente MUST NOT recomeçar a série: mesa nova é reiniciar o servidor.

#### Scenario: o fim do jogo aparece na mesa
- **WHEN** o snapshot traz `encerrado` verdadeiro, `partidas == [4, 2]` e `vencedor == 0`
- **THEN** a mesa mostra o fim do jogo, `Ana e Caio` (assentos 0 e 2) como a dupla vencedora e o placar final `4 x 2`

#### Scenario: a mesa encerrada não anuncia vez
- **WHEN** o snapshot traz `encerrado` verdadeiro e `vez` preenchido com o assento do jogador
- **THEN** o `#aviso` não mostra `Sua vez` e não chama ninguém para jogar

#### Scenario: a mesa encerrada não manda jogar
- **WHEN** o snapshot traz `encerrado` verdadeiro e o jogador aperta `Enter`
- **THEN** o cliente não manda `jogar` e nenhum motivo de recusa aparece no `#aviso`

#### Scenario: EDGE - o nome ausente cai para a dupla
- **WHEN** o snapshot traz `encerrado` verdadeiro, `vencedor == 1` e o assento 3 sem nome
- **THEN** a mesa mostra `dupla 1–3` como vencedora, sem nome vazio nem `None`

#### Scenario: EDGE - o jogo em andamento segue mostrando o placar simples
- **WHEN** o snapshot traz `encerrado` falso com `partidas == [1, 2]`
- **THEN** a mesa mostra o placar `1 x 2` sem anúncio de fim de jogo

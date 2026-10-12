# Lições Aprendidas — PYSUECA-V1

> **Iniciativa:** `pi-spec/pysueca-v1/`
> **PLANO:** `pi-spec/pysueca-v1/PLANO-PYSUECA-V1.md`
> Arquivo append-only — cada sprint acrescenta uma seção ao final. Nunca sobrescreva.

---

## Sprint 01-carta-e-baralho — Carta e baralho — 2026-10-12

**Aprendizado:** a aritmética de carta fechou numa tabela única em `Valor` (`pontos`/`forca` como dados do enum), e a assinatura `vence(outra, naipe_puxado, trunfo)` foi decidida antes de codar — o grill pegou o furo do vaza de três naipes (descarte de força maior vencendo o naipe puxado). Por outro lado, `carta.py` nasceu completo demais: 4 cenários (pontos, força, texto) não chegaram a ficar vermelhos, viraram só cobertura.

**O que muda nas próximas sprints:** escrever a 1ª versão do módulo com o mínimo que faz o tracer bullet passar (ex.: `Naipe`/`Valor` sem `pontos`/`forca`/`de_texto`) e adicionar cada campo no seu ciclo RED→GREEN, para todo cenário do qa-plan ter um vermelho de verdade.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Teste do guard de tamanho de `de_texto` (`carta.py:80`) | baixa | ramo defensivo de 1 linha; cobrir no próximo teste de `carta.py` |
| Teste de `Carta.__str__` (`carta.py:75`) | baixa | sem consumidor até a sprint 06; cobrir quando a TUI usar |

**Evidências:** `pi-spec/pysueca-v1/execucao/01-carta-e-baralho/relatorio-verificacao.md`

---

## Sprint 01-carta-e-baralho — Re-verificação (retrabalho) — 2026-10-12

**Aprendizado:** os dois gaps de cobertura da primeira verificação fecharam num ciclo curto, sem mudar comportamento: `Carta.__str__` saiu (YAGNI, sem consumidor) e o guard de tamanho de `de_texto` ganhou EDGE (`"7HH"`/`"7"`/`""` → `ValueError`). `carta.py` e `baralho.py` ficaram em 100% de cobertura.

**O que muda nas próximas sprints:** retrabalho de verificação deve ficar restrito a teste/limpeza quando o motor já está correto; o ciclo `grill → atualizar → implementar → verificar` reabre sem atrito.

**Retrabalho adiado:** nenhum desta sprint. Resta só `uv run mypy src` vermelho por `main.py:52` (pré-existente), endereçado na sprint 06 que reescreve `main.py`.

**Evidências:** `pi-spec/pysueca-v1/execucao/01-carta-e-baralho/relatorio-verificacao.md`

---

## Sprint 02-vaza-e-mao — Vaza e mão — 2026-10-12

**Aprendizado:** a `Mao` como máquina de estados explícita (`preparar` → 10 vazas → `pontos`/`resultado`) fechou com 100% de cobertura de `motor.py` e sem reimplementar precedência — `Vaza.vencedor` só agrega `Carta.vence`, então os cenários de desempate (trunfo, entre trunfos, descarte) nasceram verdes. O refactor `_validar` (task 7.1) tornou explícito o invariante "validar tudo antes de mutar" e sustenta o EDGE "jogada ilegal não altera o estado". O que **não** funcionou: de novo o módulo cresceu antes do 1º vermelho — os cenários `4.7` (trunfar sem o naipe) e `5.4` (quilo/bandeira) foram marcados RED, mas a implementação adjacente já os cobria e eles viraram só cobertura, repetindo a lição da sprint 01.

**O que muda nas próximas sprints:** implementar exatamente o ramo que o teste pede e deixar o outro ramo para o próximo RED — em `jogada_legal`, o 1º GREEN deveria ter sido `return carta.naipe is naipe_puxado` (recusa o outro naipe) e o ramo "mão sem o naipe → libera" só vir no teste 4.7; em `Resultado.de_pontos`, o 1º GREEN só com empate/normal e os limites 91/119/120 no teste 5.4. Reduzir o escopo do `feat(...)` ao mínimo que faz o teste atual passar.

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Registrar/reforçar o vício de "RED esperado verde" por implementação antecipada (4.7, 5.4) | média | reduz o sinal dos testes das sprints 03–06; virou padrão recorrente desde a sprint 01 |
| Atualizar a linha de decisão arquitetural do PLANO (`puxar` fundido em `Mao.jogar`, decisão 2 do `design.md`) | baixa | leitura do PLANO diverge do design; sem custo de execução |
| Fechar `mypy src` (`main.py:52`) e `ruff check` (`main.py` RUF012, `imagens/get_images.py` I001) | baixa | pré-existentes, endereçados na sprint 06 que reescreve `main.py` |

**Evidências:** `pi-spec/pysueca-v1/execucao/02-vaza-e-mao/relatorio-verificacao.md`

---

## Sprint 03-jogo-e-papeis — Jogo e papéis — 2026-10-12

**Aprendizado:** o `Jogo` fechou como dono único da mesa (`preparar`/`jogar`/`encerrar_mao` + placar + `encerrado`/`vencedor`) reaproveitando `Mao`/`Vaza` sem tocar na sprint 02 — `motor.py` ficou em 99% de cobertura e `test_jogo.py` com 11 testes. O RED fez o seu trabalho de verdade uma vez: o teste de quilo (`test_quilo_soma_duas_partidas_a_dupla_1`) **falhou** porque o próprio `qa-plan.md` trazia `41 a 79`, que é vitória normal, não quilo; o vermelho revelou o defeito do artefato antes de virar código errado (`29 a 91` é quilo). O que de novo **não** funcionou: repetiu-se o "RED esperado verde" (tasks 2.4, 4.4, 4.7, 6.4, 6.7), agora explícito no `tasks.md` como cobertura — sinal de teste ainda fraco na 3ª sprint seguida.

**O que muda nas próximas sprints:** tratar os cenários de cobertura declarados no `qa-plan.md` como EDGE de ramo (não como RED independente) e, ao escrever o teste, cobrir de fato o ramo novo — o cenário de empate 60–60 só ficou observável depois de receber as asserções de rotação (`5.1`) e `encerrado is False` (`6.1`), que ficaram vermelhas junto do seu GREEN. Sempre que um teste de placar falhar, desconfiar primeiro da aritmética do artefato (soma 120, faixa 91–119 para quilo).

**Retrabalho adiado:**

| O que | Criticidade (alta\|média\|baixa) | Impacto se adiar |
|---|---|---|
| Ancorar `Jogo.vencedor is None` enquanto o jogo corre (`motor.py:183`, única linha descoberta) | baixa | contrato documentado sem teste; protocolo (04) e TUI (06) trazem seus próprios testes |
| `ruff`/`mypy` vermelhos em `main.py` e `imagens/get_images.py` | baixa | pré-existentes desde a sprint 01; `main.py` é reescrita na sprint 06 |

**Evidências:** `pi-spec/pysueca-v1/execucao/03-jogo-e-papeis/relatorio-verificacao.md`

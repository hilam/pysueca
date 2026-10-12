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

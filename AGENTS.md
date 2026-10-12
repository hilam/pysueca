# AGENTS.md — pysueca

Sueca para quatro jogadores: um servidor headless dono das regras e clientes Textual que mandam intenções e desenham o estado recebido.

Regras em `README.md`, vocabulário em `CONTEXT.md`, decisões em `docs/adr/`.

## Comandos

- `uv run pytest` — suite completa
- `uv run pytest tests/test_carta.py -q` — um arquivo de teste
- `uv run pytest --cov=pysueca --cov-fail-under=80` — suite com o gate de cobertura
- `uv run ruff check` e `uv run ruff format --check` — lint e formatação
- `uv run mypy src` — tipos

## Mapa de arquivos

- `src/pysueca/carta.py` — `Naipe`, `Valor`, `Carta`: pontos, força, texto `"7H"` ida-e-volta e `vence(outra, naipe_puxado, trunfo)`
- `src/pysueca/baralho.py` — as 40 cartas e `embaralhar()`, com `random.Random` injetado
- `src/pysueca/motor.py` — `Vaza`, `Mao`, `Jogo`, `Resultado` e `ErroJogada`: as regras puras e síncronas
- `src/pysueca/protocolo.py` — as mensagens de fio, o codec JSON (`serializar`/`desserializar`), a validação estrita e o snapshot `estado` por assento
- `src/pysueca/main.py` — esqueleto Textual (substituído na sprint 06)
- `docs/imagens/` — PNGs sem uso, material para um modo imagem futuro
- `tests/` — testes do motor puro
- `docs/adr/` — decisões arquiteturais (0001–0005)
- `pi-spec/` — plano e sprints

## Invariantes

- **Motor puro e síncrono**: `carta.py`, `baralho.py`, `motor.py` e `protocolo.py` não usam `asyncio`, rede nem Textual.
- **Só Textual**: nenhuma dependência de terceiros além do Textual; o resto é stdlib (`docs/adr/0004`).

## Convenções

- Ciclo TDD: Red → Green → Refactor, com commits `test(...)` / `feat(...)` / `refactor(...)` usando o scope da sprint.
- O domínio é em português (`Naipe`, `Valor`, `Carta`, `Baralho`); `SHALL`/`MUST` ficam em inglês nos specs.
- `pyproject.toml:12` tem um entrypoint quebrado (`pysueca:src.pysueca.main`), corrigido na sprint 06.

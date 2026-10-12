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
- `src/pysueca/servidor.py` — a única casca `asyncio`: os quatro assentos (nome e conexão), as intenções validadas pelo motor, o broadcast do snapshot por assento, a queda que congela e reserva, a reconexão pelo nome e o teto de bytes do protocolo
- `src/pysueca/main.py` — o cliente Textual: o worker `@work` que lê o fio e traduz em `mostrar_estado`/`avisar`, os painéis `#aviso`, `#assentos`, `#mesa` e `#mao`, as teclas de seleção/jogada e o `RespostaScreen` do cima ou baixo
- `docs/imagens/` — PNGs sem uso, material para um modo imagem futuro
- `tests/` — testes do motor puro, do protocolo, do servidor e do cliente
- `docs/adr/` — decisões arquiteturais (0001–0005)
- `pi-spec/` — plano e sprints

## Invariantes

- **Motor puro e síncrono**: `carta.py`, `baralho.py`, `motor.py` e `protocolo.py` não usam `asyncio`, rede nem Textual.
- **Só as cascas `asyncio` tocam a rede**: `servidor.py` (dono da mesa) e `main.py` (cliente) são as únicas cascas do projeto; o motor e o protocolo não.
- **Nenhum widget conhece o protocolo**: no cliente, só o worker importa `protocolo.py`; ele traduz a mensagem para método de tela (`mostrar_estado`/`avisar`) antes de qualquer `Widget.update`.
- **Só Textual**: nenhuma dependência de terceiros além do Textual; o resto é stdlib (`docs/adr/0004`).

## Convenções

- Ciclo TDD: Red → Green → Refactor, com commits `test(...)` / `feat(...)` / `refactor(...)` usando o scope da sprint.
- O domínio é em português (`Naipe`, `Valor`, `Carta`, `Baralho`); `SHALL`/`MUST` ficam em inglês nos specs.
- Dois entrypoints: `pysueca` (`pysueca.main:main`, cliente) e `pysueca-servidor` (`pysueca.servidor:main`), ambos com `argparse` e defaults `127.0.0.1:8765`.

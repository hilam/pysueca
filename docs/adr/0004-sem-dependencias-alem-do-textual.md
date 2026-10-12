# Nenhuma dependência além do Textual, e as cartas são texto

O cliente desenha as cartas em texto (`A♥`, `7♠`), colorindo copas e ouros, porque o Textual 8.2.8 não tem widget de imagem: exibir os PNGs de `src/pysueca/imagens/` exigiria a dependência `textual-image` ou implementar o protocolo de imagem do terminal à mão. As imagens ficam no repositório como material para um modo imagem futuro. Todo o resto do projeto usa apenas a stdlib (`asyncio`, `json`, `random`, `enum`, `dataclasses`).

from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header


class SuecaApp(App):
    """
    Um jogo de cartas
    """
    PATH_IMAGENS = Path('./imagens')

    NAIPES = {
        'club': 'paus',
        'heart': 'copas',
        'spade': 'espadas',
        'diamond': 'ouros'
    }

    CARTAS = {
        'A': 'Ás',
        '7': 'sete',
        'K': 'rei',
        'J': 'valete',
        'Q': 'rainha',
        '6': 'seis',
        '5': 'cinco',
        '4': 'qiatro',
        '3': 'três',
        '2': 'dois'
    }

    def compose(self) -> ComposeResult:
        """Compose our UI."""
        yield Header()
        yield Container(
            # DirectoryTree(path, id="tree-view"),
            # Vertical(Static(id="code", expand=True), id="code-view"),
        )
        yield Footer()


if __name__ == "__main__":
    SuecaApp().run()

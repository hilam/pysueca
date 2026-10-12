from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header


class SuecaApp(App):
    """
    Um jogo de cartas
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Sair", priority=True),
        Binding("d", "toggle_dark", "Dark/Light"),
    ]

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
        yield Header(show_clock=True)
        yield Container(
            # DirectoryTree(path, id="tree-view"),
            # Vertical(Static(id="code", expand=True), id="code-view"),
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = SuecaApp()
    app.run()

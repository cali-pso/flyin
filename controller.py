from parser import Parser

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.color import Color

from textual_canvas import Canvas


class Controller(App):
    BINDINGS = [("d", "toggle_light", "Toggle light mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Canvas(1800, 1050, Color(0, 119, 0), id="bigger")
        yield Footer()

    def action_toggle_light(self) -> None:
        """An action to toggle light mode."""

        self.theme = (
            "textual-dark"
            if self.theme == "textual-light"
            else "textual-light"
        )

    def on_mount(self) -> None:
        self.init_parser()
        for hub in self.parser.hubs:
            self.query_one(Canvas).set_pixel(hub.x * 10, hub.y * 10)

    def init_parser(self) -> None:
        self.parser = Parser()
        self.parser.parse_file()

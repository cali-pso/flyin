from parser import Parser
from tmap import TMap

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.color import Color

from textual_canvas import Canvas


class Controller(App):
    CSS_PATH = ["visualiser.tcss"]
    BINDINGS = [("d", "toggle_light", "Toggle light mode")]
    SIZE = 20

    def compose(self) -> ComposeResult:
        yield Header()
        yield TMap(self.init_parser(), self.SIZE)
        yield Footer()

    def action_toggle_light(self) -> None:
        """An action to toggle light mode."""

        self.theme = (
            "textual-dark"
            if self.theme == "textual-light"
            else "textual-light"
        )

    def on_mount(self) -> None:
        for connection in self.parser.connections:
            start_x, start_y = (
                connection.start_node.x * self.SIZE,
                connection.start_node.y * self.SIZE,
            )
            end_x, end_y = (
                connection.end_node.x * self.SIZE,
                connection.end_node.y * self.SIZE,
            )
            self.query_one(Canvas).draw_line(start_x, start_y, end_x, end_y)
        for hub in self.parser.hubs:
            self.query_one(Canvas).set_pixel(
                hub.x * self.SIZE, hub.y * self.SIZE, Color.parse("red")
            )

    def init_parser(self) -> Parser:
        self.parser = Parser()
        self.parser.parse_file()
        return self.parser

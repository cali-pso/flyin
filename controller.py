from parser import Parser
from map import Map
from tmap import TMap
from pathfinder import PathFinder
from reservation_table import ReservationTable
from hubs import Hub

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.color import Color

from textual_canvas import Canvas
from time import sleep


class Controller(App):
    CSS_PATH = ["visualiser.tcss"]
    BINDINGS = [
        ("d", "toggle_light", "Toggle light mode"),
        ("s", "start_simulation", "Start simulation"),
    ]
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

    def action_start_simulation(self) -> None:
        path_finder = PathFinder(self.map)
        self.paths: list[list[Hub]] = list()
        table = ReservationTable(self.map)
        for i in range(0, self.map.nb_drones):
            self.paths.append(path_finder.find_path("start", "goal", 0, table))
        for path in self.paths:
            for hub in path:
                self.query_one(Canvas).set_pixel(
                    hub.x * self.SIZE, hub.y * self.SIZE, Color.parse("blue")
                )
        self.turns = max([len(path) for path in self.paths])

    def on_mount(self) -> None:
        for connection in self.map.connections:
            start_x, start_y = (
                connection.start_node.x * self.SIZE,
                connection.start_node.y * self.SIZE,
            )
            end_x, end_y = (
                connection.end_node.x * self.SIZE,
                connection.end_node.y * self.SIZE,
            )
            self.query_one(Canvas).draw_line(start_x, start_y, end_x, end_y)
        for hub in self.map.hubs:
            self.query_one(Canvas).set_pixel(
                hub.x * self.SIZE, hub.y * self.SIZE, Color.parse("red")
            )

    def init_parser(self) -> Parser:
        self.parser = Parser()
        self.parser.parse_file()
        self.map = Map(self.parser)
        return self.map

from map import Map

from textual.widget import Widget
from textual.color import Color
from textual_canvas import Canvas


class TMap(Widget):
    def __init__(self, map: Map, size_factor: int) -> None:
        super().__init__()
        size = (
            max([hub.x for hub in map.hubs]),
            max([hub.y for hub in map.hubs]),
        )
        self._canvas = Canvas(
            size[0] * size_factor + 1,
            size[1] * size_factor + 1,
            Color(0, 119, 0),
        )

    def compose(self) -> None:
        yield self._canvas

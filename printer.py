from hubs import Hub
from connections import Connection

from termcolor import cprint  # type: ignore [import-not-found]
from typing import Optional


class Printer:
    """Formats and prints drone paths turn-by-turn."""

    def __init__(
        self,
        paths: list[list[Hub | Connection]],
        connections_dict: dict[Connection, str],
    ) -> None:
        """Initializes the Printer with paths and connection mappings."""
        self.paths = paths
        self.connections_dict = connections_dict
        self.turns = max([len(i) for i in self.paths])
        self.paths_by_turn: dict[int, list[Optional[Hub | Connection]]] = {
            i: [(h[i] if len(h) > i else None) for h in self.paths]
            for i in range(self.turns)
            if i > 0
        }
        color_prints_list = [
            (lambda text: cprint(f"{text}", (255, 161, 0), end=" ")),
            (lambda text: cprint(f"{text}", (69, 13, 13), end=" ")),
            (lambda text: cprint(f"{text}", (128, 108, 26), end=" ")),
            (lambda text: cprint(f"{text}", (103, 32, 173), end=" ")),
            (lambda text: cprint(f"{text}", (102, 0, 0), end=" ")),
            (lambda text: cprint(f"{text}", (169, 0, 204), end=" ")),
            (lambda text: cprint(f"{text}", (0, 255, 68), end=" ")),
            (lambda text: self.print_rainbow(text)),
        ]

        self.fancy_colors_print = {
            "orange": color_prints_list[0],
            "crimson": color_prints_list[1],
            "gold": color_prints_list[2],
            "purple": color_prints_list[3],
            "darkred": color_prints_list[4],
            "violet": color_prints_list[5],
            "lime": color_prints_list[6],
            "rainbow": color_prints_list[7],
        }

    def print(self) -> None:
        """Prints the movements of each active drone for all turns."""
        for turn in range(1, self.turns):
            printed_this_turn = False

            for y, hub in enumerate(self.paths_by_turn[turn]):
                if hub is None:
                    continue

                prev_hub = self.paths_by_turn[turn - 1][y] if turn > 1 else 0

                if prev_hub != hub:
                    printed_this_turn = True

                    if isinstance(hub, Hub):
                        name = hub.name
                        color = hub.color
                    else:
                        name = self.connections_dict[hub]
                        color = "white"

                    # FIX: Use 'y + 1' for the Drone ID
                    if color in self.fancy_colors_print:
                        self.fancy_colors_print[color](f"D{y + 1}-{name}")
                    else:
                        cprint(f"D{y + 1}-{name}", color, end=" ")

            if printed_this_turn and turn < self.turns:
                print()

    @staticmethod
    def print_rainbow(text: str, ending: str = " ") -> None:
        """Prints text in rainbow colors."""
        rainbow_colors = [
            (255, 0, 0),  # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (75, 0, 130),  # Indigo
            (148, 0, 211),  # Violet
        ]

        for i, char in enumerate(text):
            color = rainbow_colors[i % len(rainbow_colors)]
            cprint(char, color, end="")

        # Apply the final ending character (e.g., a space or a newline)
        print(end=ending)

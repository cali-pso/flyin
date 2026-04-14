from hubs import Hub

from typing import Any


class Connection:
    def __init__(
        self, start_node: Hub, end_node: Hub, max_link_capacity: int = None
    ):
        self.start_node = start_node
        self.end_node = end_node
        self.max_link_capacity = max_link_capacity


class PatchBayValidator:
    def __init__(self, connections: list[Connection]) -> Any:
        self.connections = connections

    def check_duplicates(self) -> Any:
        pairs: list[tuple[Hub, Hub]] = list()
        for connection in self.connections:
            pairs.append((connection.start_node, connection.end_node))

        for pair in pairs:
            if (pair[1], pair[0]) in pairs or len(
                [p for p in pairs if p == pair]
            ) > 1:
                raise ValueError(f"duplicate connection {pair[0]}-{pair[1]}")

        return self

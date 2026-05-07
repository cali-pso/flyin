from hubs import Hub

from typing import Any, Optional


class Connection:
    def __init__(
        self,
        start_node: Hub,
        end_node: Hub,
        max_link_capacity: Optional[int] = None,
    ):
        self.start_node = start_node
        self.end_node = end_node
        self.max_link_capacity = max_link_capacity


class PatchBayValidator:
    def __init__(self, connections: list[Connection], hubs: list[Hub]) -> None:
        self.connections = connections
        self.hubs = hubs

    def check_duplicates(self) -> Any:
        pairs: list[tuple[Hub, Hub]] = list()
        for connection in self.connections:
            pairs.append((connection.start_node, connection.end_node))

        for pair in pairs:
            if (pair[1], pair[0]) in pairs or len(
                [p for p in pairs if p == pair]
            ) > 1:
                raise ValueError(f"duplicate connection {pair[0]}-{pair[1]}")

        names_set = {hub.name for hub in self.hubs}
        names_list = [hub.name for hub in self.hubs]
        if len(names_set) != len(names_list):
            raise ValueError("duplicate hubs")

        return self

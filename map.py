from hubs import Hub
from connections import Connection
from parser import Parser

from typing import Optional


class Map:
    def __init__(self, parser: Parser) -> None:
        self.nb_drones = parser.nb_drones
        self.hubs: list[Hub] = parser.hubs
        self.connections: list[Connection] = parser.connections

    @staticmethod
    def get_connection_from_obj(connec: Connection) -> str:
        return f"{connec.start_node.name}-{connec.end_node.name}"

    def get_connection_from_str(
        self, start_node_name: str, end_node_name: str
    ) -> Optional[str]:
        node_names = sorted([start_node_name, end_node_name])
        for connec in self.connections:
            connec_node_names = sorted(
                [connec.start_node.name, connec.end_node.name]
            )
            if (
                connec_node_names[0] == node_names[0]
                and connec_node_names[1] == node_names[1]
            ):
                return self.get_connection_from_obj(connec)
        raise ValueError(
            f"No connection between {node_names[0]} and {node_names[1]}"
        )

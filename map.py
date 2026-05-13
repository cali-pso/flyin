from hubs import Hub, StartHub, EndHub
from connections import Connection
from parser import Parser


class Map:
    """Store and process useful graph related data/structures

    Attributes:
        - nb_drones: drones to simulate
        - hubs: list of Hubs (nodes)
        - connections: list of Connections (edges)
        - start_hub: start node
        - end_hub: end node
        - graph: dict with each hub as a key and hub's neighbours as a value

    """

    def __init__(self, parser: Parser) -> None:
        """Fetch and store information from parser"""
        self.nb_drones = parser.nb_drones
        self.hubs: list[Hub] = parser.hubs
        self.start_hub = [i for i in self.hubs if isinstance(i, StartHub)][0]
        self.end_hub = [i for i in self.hubs if isinstance(i, EndHub)][0]
        self.connections: list[Connection] = parser.connections

        self.graph: dict[str, list[Hub]] = {hub.name: [] for hub in self.hubs}
        for conn in self.connections:
            self.graph[conn.start_node.name].append(conn.end_node)
            self.graph[conn.end_node.name].append(conn.start_node)

    @staticmethod
    def get_connection_from_obj(connec: Connection) -> str:
        """Return connection name (string) from passed Connection instance"""
        return f"{connec.start_node.name}-{connec.end_node.name}"

    def get_connection_from_str(
        self, start_node_name: str, end_node_name: str
    ) -> str:
        """Return connection instance from passed strings"""
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

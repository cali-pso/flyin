from parser import Parser
from connections import Connection
from hubs import StartHub, EndHub

from typing import Dict


class ReservationTable:
    """
    Tracks space-time reservations to prevent drone collisions.
    """

    def __init__(self, parser: Parser) -> None:
        self.table: Dict[int, Dict[str, int]] = dict()
        self.capacities: Dict[str, float | int] = dict()

        self._init_capacities(parser)

    def _init_capacities(self, parser: Parser) -> None:
        """Create table of maximum capacities for hubs and connections"""

        for hub in parser.hubs:
            if isinstance(hub, StartHub) or isinstance(hub, EndHub):
                self.capacities[hub.name] = float("inf")
            else:
                self.capacities[hub.name] = getattr(hub, "max_drones", 1)

        for connec in parser.connections:
            connec_name = self.get_connection_name(connec)
            capacity = getattr(connec, "max_link_capacity", 1)
            self.capacities[connec_name] = capacity

    @staticmethod
    def get_connection_name(connec: Connection) -> str:
        return f"{connec.start_node.name}-{connec.end_node.name}"

    def get_occupancy(self, turn: int, location: str) -> int:
        if turn not in self.table:
            return 0
        return self.table[turn].get(location, 0)

    def is_available(self, turn: int, location: str) -> bool:

        if location not in self.capacities:
            raise ValueError(
                f"Location {location} does not exist in the network."
            )

        occupancy = self.get_occupancy(turn, location)
        capacity = self.capacities[location]

        return occupancy < capacity

    def reserve(self, turn: int, location: str) -> None:

        if not self.is_available(turn, location):
            raise ValueError(
                f"Cannot reserve {location} at turn {turn}: Capacity full."
            )

        if not self.table.get(turn):
            self.table[turn] = dict()
        elif not self.table[turn].get(location):
            self.table[turn][location] = 0

        self.table[turn][location] += 1

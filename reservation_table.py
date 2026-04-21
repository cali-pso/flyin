from map import Map
from hubs import StartHub, EndHub

from typing import Dict


class ReservationTable:
    """
    Tracks space-time reservations to prevent drone collisions.
    """

    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.table: Dict[int, Dict[str, int]] = dict()
        self.capacities: Dict[str, float | int] = dict()

        self._init_capacities()

    def _init_capacities(self) -> None:
        """Create table of maximum capacities for hubs and connections"""

        for hub in self.map.hubs:
            if (
                isinstance(hub, StartHub)
                or isinstance(hub, EndHub)
                or not hub.max_drones
            ):
                self.capacities[hub.name] = float("inf")
            else:
                self.capacities[hub.name] = getattr(hub, "max_drones", 1)

        for connec in self.map.connections:
            connec_name = self.map.get_connection_from_obj(connec)
            capacity = getattr(connec, "max_link_capacity", 1)
            if not capacity:
                capacity = float('inf')
            self.capacities[connec_name] = capacity

    def get_occupancy(self, turn: int, location: str) -> int:
        if turn not in self.table:
            return 0
        return self.table[turn].get(location, 0)

    def is_available(self, turn: int, location: str) -> bool:

        if location not in self.capacities:
            raise ValueError(
                f"Location {location} does not exist in the network.\n\n{self.capacities}"
            )

        occupancy = self.get_occupancy(turn, location)
        capacity = self.capacities[location]

        if not capacity:
            return True

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

from map import Map
from hubs import Hub
from connections import Connection
from reservation_table import ReservationTable

from dataclasses import dataclass, field
from collections import deque
from typing import List, Dict

import heapq


@dataclass(order=True)
class SearchState:
    """
    Represents a specific state in the A* search tree.
    Ordered by the estimated total cost (f_score).
    """

    f_score: int  # f(n) = g(n) + h(n). Used for priority queue sorting.
    turn: int = field(compare=False)  # g(n) = actual turns taken so far.
    current_hub_name: str = field(compare=False)
    path_history: List[str] = field(compare=False)


class PathFinder:
    def __init__(self, map: Map):
        self.map = map
        self.locations_dict: Dict[str, Hub | Connection] = {
            hub.name: hub for hub in map.hubs
        }
        self.locations_dict.update(
            {
                map.get_connection_from_obj(conn): conn
                for conn in map.connections
            }
        )

        self.graph = map.graph

    def heuristic(self, current_hub: Hub, goal_hub: Hub) -> int:
        """
        Calculates the Manhattan distance between two hubs.
        Acts as h(n) for the A* algorithm.
        """
        return abs(current_hub.x - goal_hub.x) + abs(
            current_hub.y - goal_hub.y
        )

    def find_path(
        self,
        start_name: str,
        goal_name: str,
        start_turn: int,
        reservation_table: ReservationTable,
    ) -> List[Hub | Connection]:

        start_hub = self.locations_dict[start_name]
        goal_hub = self.locations_dict[goal_name]

        assert isinstance(start_hub, Hub)
        assert isinstance(goal_hub, Hub)

        open_set: list[SearchState] = []
        initial_h = self.heuristic(start_hub, goal_hub)
        heapq.heappush(
            open_set,
            SearchState(initial_h, start_turn, start_name, [start_name]),
        )

        visited = set()

        while open_set:
            current_state = heapq.heappop(open_set)

            # Goal Check
            if current_state.current_hub_name == goal_name:
                for i, loc in enumerate(current_state.path_history):
                    reservation_table.reserve(i, loc)
                return [
                    self.locations_dict[i] for i in current_state.path_history
                ]

            # Mark as visited for this specific point in time
            state_key = (current_state.current_hub_name, current_state.turn)
            if state_key in visited:
                continue
            visited.add(state_key)

            # Option 1: WAIT action. Stay at the current hub for 1 turn.
            next_turn = current_state.turn + 1
            if reservation_table.is_available(
                next_turn, current_state.current_hub_name
            ):
                current_hub_obj = self.locations_dict[
                    current_state.current_hub_name
                ]
                assert isinstance(current_hub_obj, Hub)
                wait_h = self.heuristic(
                    current_hub_obj,
                    goal_hub,
                )
                wait_f = next_turn + wait_h
                heapq.heappush(
                    open_set,
                    SearchState(
                        wait_f,
                        next_turn,
                        current_state.current_hub_name,
                        current_state.path_history
                        + [current_state.current_hub_name],
                    ),
                )

            # Explore moving options (wether neighbour is restricted or not)
            for neighbor in self.graph[current_state.current_hub_name]:
                if neighbor.zone == "blocked":
                    continue

                conn_name = self.map.get_connection_from_str(
                    current_state.current_hub_name, neighbor.name
                )

                if neighbor.zone == "restricted":
                    arrival_turn = current_state.turn + 2

                    if reservation_table.is_available(
                        current_state.turn + 1, conn_name
                    ) and reservation_table.is_available(
                        arrival_turn, neighbor.name
                    ):
                        move_h = self.heuristic(neighbor, goal_hub)
                        new_path = current_state.path_history + [
                            conn_name,
                            neighbor.name,
                        ]
                        heapq.heappush(
                            open_set,
                            SearchState(
                                arrival_turn + move_h,
                                arrival_turn,
                                neighbor.name,
                                new_path,
                            ),
                        )

                else:
                    arrival_turn = current_state.turn + 1

                    if reservation_table.is_available(
                        arrival_turn, conn_name
                    ) and reservation_table.is_available(
                        arrival_turn, neighbor.name
                    ):
                        move_h = self.heuristic(neighbor, goal_hub)
                        priority_discount = (
                            -1 if neighbor.zone == "priority" else 0
                        )
                        f_score = arrival_turn + move_h + priority_discount

                        new_path = current_state.path_history + [neighbor.name]
                        heapq.heappush(
                            open_set,
                            SearchState(
                                f_score, arrival_turn, neighbor.name, new_path
                            ),
                        )

        raise PathNotFoundError()


class Scout:
    def __init__(self, map: Map) -> None:
        self.graph = map.graph
        self.start_name = map.start_hub.name
        self.end_name = map.end_hub.name

    def is_solvable(self) -> None:
        """
        Uses BFS to verify if a physical path exists between start and goal,
        ignoring all temporal constraints and reservations.
        """
        visited = set([self.start_name])
        queue = deque([self.start_name])

        while queue:
            current_name = queue.popleft()

            if current_name == self.end_name:
                print("what")
                return

            for neighbor in self.graph[current_name]:
                if neighbor.zone == "blocked":
                    continue

                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append(neighbor.name)

        raise PathNotFoundError("map is not solvable")


class PathNotFoundError(Exception):
    pass

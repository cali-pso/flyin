class Drone:
    def __init__(self, drone_id: int, current_hub: Hub):
        self.id = f"D{drone_id}"
        self.current_hub = current_hub
        self.is_delivered = False
        self.transit_turns_remaining = (
            0  # Crucial for handling restricted zones
        )


class SimulationEngine:
    def __init__(self, parser: Parser):
        self.hubs = parser.hubs
        self.connections = parser.connections
        self.drones = [
            Drone(i + 1, self.get_start_hub()) for i in range(parser.nb_drones)
        ]
        self.turn_count = 0

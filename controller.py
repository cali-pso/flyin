from parser import Parser
from map import Map
from pathfinder import PathFinder
from reservation_table import ReservationTable
from hubs import Hub
from visualiser import Visualiser
from printer import Printer


class Controller:
    def __init__(self) -> None:
        pass

    def run_parser(self) -> None:
        parser = Parser()
        parser.parse_file()
        self.map = Map(parser)

    def run_simulation(self) -> None:
        pathfinder = PathFinder(self.map)
        table = ReservationTable(self.map)
        self.paths: list[list[Hub]] = list()
        for i in range(0, self.map.nb_drones):
            self.paths.append(
                pathfinder.find_path(
                    self.map.start_hub.name, self.map.end_hub.name, 0, table
                )
            )
        self.turns = max([len(i) for i in self.paths]) - 1

    def run_visualiser(self) -> None:
        visualiser = Visualiser(self.map, self.paths)
        visualiser.run()

    def run_printer(self) -> None:
        connections_dict = {
            connec: name
            for name in [
                self.map.get_connection_from_obj(n) for n in self.map.connections
            ]
            for connec in self.map.connections
        }
        printer = Printer(self.paths, connections_dict)
        printer.print()

from parser import Parser
from map import Map
from pathfinder import PathFinder
from reservation_table import ReservationTable
from hubs import Hub
from connections import Connection
from visualiser import Visualiser
from printer import Printer
from errors import (
    ParsingError,
    PathFindingError,
    PrintingError,
    VisualisingError,
)


class Controller:
    def __init__(self) -> None:
        pass

    def run_parser(self) -> None:
        try:
            parser = Parser()
            parser.parse_file()
            self.map = Map(parser)
        except Exception as e:
            raise ParsingError(e)

    def run_simulation(self) -> None:
        try:
            pathfinder = PathFinder(self.map)
            table = ReservationTable(self.map)
            self.paths: list[list[Hub | Connection]] = list()
            for i in range(0, self.map.nb_drones):
                self.paths.append(
                    pathfinder.find_path(
                        self.map.start_hub.name,
                        self.map.end_hub.name,
                        0,
                        table,
                    )
                )
            self.turns = max([len(i) for i in self.paths]) - 1
        except Exception as e:
            raise PathFindingError(e)

    def run_visualiser(self) -> None:
        try:
            visualiser = Visualiser(self.map, self.paths)
            visualiser.run()
        except Exception as e:
            raise VisualisingError(e)

    def run_printer(self) -> None:
        try:
            connections_dict = {
                connec: name
                for name in [
                    self.map.get_connection_from_obj(n)
                    for n in self.map.connections
                ]
                for connec in self.map.connections
            }
            printer = Printer(self.paths, connections_dict)
            printer.print()
        except Exception as e:
            raise PrintingError(e)

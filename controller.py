from parser import Parser
from map import Map
from pathfinder import PathFinder
from reservation_table import ReservationTable
from hubs import Hub
from visualiser import Visualiser


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
            self.paths.append(pathfinder.find_path(self.map.start_hub.name, self.map.end_hub.name, 0, table))
        self.turns = max([len(i) for i in self.paths])

    def run_visualiser(self) -> None:
        visualiser = Visualiser(self.map, self.paths)
        visualiser.run()

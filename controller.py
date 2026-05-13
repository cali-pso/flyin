from parser import Parser
from map import Map
from pathfinder import PathFinder, Scout
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

import argparse


class Controller:
    """
    Initialize manage and run core components of the program

    Attributes:
        - map_filename: taken from command line to parser
        - run_visual_bool: flag deciding wether to run visualiser
        - Map: Map instance from parser
        - paths: 2D list of paths taken by each drone
    """

    def __init__(self) -> None:
        pass

    def parse_command_line_arguments(self) -> None:
        """Look up passed arguments and store relevant information"""
        argparser = argparse.ArgumentParser()
        argparser.add_argument(
            "map", type=str, help="name of text file containing map"
        )
        argparser.add_argument(
            "-v",
            "--visual",
            action="store_true",
            help="Run pygame visualiser after printing algorithm result",
        )
        args = argparser.parse_args()
        self.map_filename = args.map
        self.run_visual_bool = args.visual

    def run_parser(self) -> None:
        """Instantiate and run parser, store map"""
        try:
            parser = Parser()
            parser.parse_file(self.map_filename)
            self.map = Map(parser)
        except Exception as e:
            raise ParsingError(e)

    def run_simulation(self) -> None:
        """
        Instantiate and run scout then pathfinder,
        storing relevant information along the way.
        """
        try:
            scout = Scout(self.map)
            scout.is_solvable()
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
        """Instantiate and run visualiser if flag is true"""
        if self.run_visual_bool:
            try:
                visualiser = Visualiser(self.map, self.paths)
                visualiser.run()
            except Exception as e:
                raise VisualisingError(e)

    def run_printer(self) -> None:
        """Instantiate and run printer"""
        try:
            connections_dict = {
                n: self.map.get_connection_from_obj(n)
                for n in self.map.connections
            }
            printer = Printer(self.paths, connections_dict)
            printer.print()
        except Exception as e:
            raise PrintingError(e)

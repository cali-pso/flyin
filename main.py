import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from controller import Controller
from connections import Connection
from parser import Parser
from map import Map

if __name__ == "__main__":
    controller = Controller()

    controller.run_parser()
    controller.run_simulation()
    controller.run_printer()
    controller.run_visualiser()

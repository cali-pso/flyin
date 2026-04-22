from controller import Controller

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

if __name__ == "__main__":
    controller = Controller()

    controller.run_parser()
    controller.run_simulation()
    controller.run_printer()
    controller.run_visualiser()

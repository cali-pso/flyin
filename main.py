from controller import Controller

from termcolor import cprint
import sys


if __name__ == "__main__":
    try:
        controller = Controller()

        controller.run_parser()
        controller.run_simulation()
        controller.run_printer()
        controller.run_visualiser()
    except Exception as e:
        cprint(f"Error: {e}", "red", file=sys.stderr)
        sys.exit()

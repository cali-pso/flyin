from controller import Controller
from errors import (
    ParsingError,
    PathFindingError,
    PrintingError,
    VisualisingError,
)

from termcolor import cprint  # type: ignore [import-not-found]
import sys


if __name__ == "__main__":
    try:
        controller = Controller()

        controller.parse_command_line_arguments()
        controller.run_parser()
        controller.run_simulation()
        controller.run_printer()
        controller.run_visualiser()
    except ParsingError as e:
        cprint(f"Error parsing: {e}", "red", file=sys.stderr)
    except PathFindingError as e:
        cprint(f"Error finding path: {e}", "red", file=sys.stderr)
    except PrintingError as e:
        cprint(f"Error printing: {e}", "red", file=sys.stderr)
    except VisualisingError as e:
        cprint(f"Error while visualising: {e}", "red", file=sys.stderr)
    except Exception as e:
        cprint(f"Error: {e}", "red", file=sys.stderr)
    finally:
        sys.exit()

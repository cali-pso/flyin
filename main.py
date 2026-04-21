from controller import Controller
from connections import Connection
from parser import Parser
from map import Map

if __name__ == "__main__":
    controller = Controller()

    controller.run_parser()
    controller.run_simulation()
    controller.run_visualiser()
    for path in controller.paths:
        for i, hub in enumerate(path):
            print(i, hub)
            if isinstance(hub, Connection):
                print(getattr(hub, "max_link_capacity", None))
        print()
    print(controller.turns)

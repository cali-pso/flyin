from controller import Controller
from parser import Parser
from map import Map

if __name__ == "__main__":
    controller = Controller()

    controller.run()
    print(controller.turns)
    for path in controller.paths:
        for hub in path:
            print(hub)
        print()

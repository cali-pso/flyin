from controller import Controller
from parser import Parser

if __name__ == "__main__":
    controller = Controller()

    controller.run()
    parser = Parser()
    parser.parse_file()
    for hub in parser.hubs:
        print(hub.x, hub.y)

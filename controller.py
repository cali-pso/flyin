from parser import Parser


class Controller:
    def __init__(self):
        pass

    def run(self) -> None:
        parser = Parser()
        config = parser.parse_file()

from typing import Dict, Any


class Parser:
    def __init__(self):
        pass

    def parse(self, config_path: str) -> Dict[Any, Any]:
        try:
            with open(config_path, "r") as fd:
                fd.write()
        except Exception:
            pass

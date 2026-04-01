from zones import Zone

import re


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def get_cleaned_lines(config_path: str) -> dict[int, str]:
        """Open given file and remove comments/trailing whitespaces"""

        cleaned: dict[int, str] = dict()

        try:
            with open(config_path, "r") as fd:
                for line_number, line in enumerate(fd):
                    if not line.startswith("#"):
                        cleaned_line = line.split("#")[0].strip()
                        if cleaned_line:
                            cleaned[line_number] = cleaned_line

        except FileNotFoundError:
            e = f"File {config_path} not found"
            raise FileNotFoundError(e)

        else:
            return cleaned

    @staticmethod
    def get_nb_drones(line: str) -> int:
        """Try getting number of drones from given line"""
        if not line.startswith("nb_drones:"):
            raise ValueError("First line must define nb_drones")

        try:
            nb_drones = int(line.split(":")[1].strip())
            if nb_drones <= 0:
                raise ValueError

        except ValueError:
            raise ValueError("nb_drones should be a valid positive integer")

        else:
            return nb_drones

    @staticmethod
    def get_zones(line: str, line_nbr: int) -> Zone:
        # Pattern explanation:
        # ^(start_hub|end_hub|hub):    Matches the prefix
        # \s+([^\s\-]+)                Matches the name (no spaces or dashes)
        # \s+(\d+)\s+(\d+)             Matches the X and Y integer coordinates
        # (?:\s+\[(.*?)\])?$           Matches optional metadata in brackets
        pattern = (
                r"^(start_hub|end_hub|hub):"
                r"\s+([^\s\-]+)"
                r"\s+(\d+)\s+(\d+)"
                r"(?:\s+\[(.*?)\])?$"
                )
        match = re.match(pattern, line)
        if not match:
            raise ValueError(f"Line {line_nbr + 1}: syntax error")

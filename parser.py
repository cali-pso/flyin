from zones import ZoneValidator

from pydantic import ValidationError
from typing import Any

import re


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def get_cleaned_lines(config_path: str) -> dict[int, str]:
        """Open given file and remove comments/trailing whitespaces"""

        cleaned: list[tuple[int, str]] = list()

        try:
            with open(config_path, "r") as fd:
                for line_number, line in enumerate(fd):
                    if not line.startswith("#"):
                        cleaned_line = line.split("#")[0].strip()
                        if cleaned_line:
                            cleaned.append((line_number, cleaned_line))

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
    def get_zone(line: str, line_nbr: int) -> Any:
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

        hub_type, hub_name, x_str, y_str, metadata_str = match.groups()
        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            raise ValueError(f"Line {line_nbr + 1}: invalid coordinates")

        metadata: dict[str, str] = dict()
        if metadata_str:
            pairs = re.findall(r"([a-zA-Z_]+)=([a-zA-Z0-9_]+)", metadata_str)
            for k, v in pairs:
                metadata[k] = v
        config_dict: dict[Any, Any] = {
            "hub_type": hub_type,
            "hub_name": hub_name,
            "x": x,
            "y": y,
            "zone": metadata.get("zone", None),
            "color": metadata.get("color", None),
            "max_drones": metadata.get("max_drones", None),
        }
        try:
            ZoneValidator.model_validate(config_dict)
        except ValidationError as e:
            raise ValueError(f"Line {line_nbr + 1}: {e['msg']}")
        except ValueError as e:
            raise ValueError(f"Line {line_nbr + 1}: {e}")

    def parse_file(self) -> Any:

        cleaned = self.get_cleaned_lines("config.txt")
        self.get_nb_drones(cleaned[0][1])
        for line in cleaned:
            print(line[1])

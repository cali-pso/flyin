from hubs import HubValidator, Hub, StartHub, EndHub
from connections import Connection, PatchBayValidator

from pydantic import ValidationError
from typing import Any
import re


class Parser:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_cleaned_lines(config_path: str) -> list[tuple[int, str]]:
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
    def parse_zone(line: str, line_nbr: int) -> dict[str, Any]:
        # Pattern explanation:
        # ^(start_hub|end_hub|hub):    Matches the prefix
        # \s+([^\s\-]+)                Matches the name (no spaces or dashes)
        # \s+(\d+)\s+(\d+)             Matches the X and Y integer coordinates
        # (?:\s+\[(.*?)\])?$           Matches optional metadata in brackets
        pattern = (
            r"^(start_hub|end_hub|hub):"
            r"\s+([^\s\-]+)"
            r"\s+(-?\d+)\s+(-?\d+)"
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
        max_drones = metadata.get("max_drones", None)
        if max_drones and int(max_drones) < 0:
            raise ValueError(
                f"Line {line_nbr + 1}: max_drones must be a positive integer"
            )
        config_dict: dict[str, Any] = {
            "hub_type": str(hub_type),
            "name": str(hub_name),
            "x": int(x),
            "y": int(y),
            "zone": metadata.get("zone", None),
            "color": metadata.get("color", None),
            "max_drones": max_drones if max_drones else 1,
        }
        return config_dict

    @staticmethod
    def get_zone(line: str, line_nbr: int) -> Hub:
        config_dict = Parser.parse_zone(line, line_nbr)
        try:
            HubValidator.model_validate(config_dict)
        except ValidationError as e:
            raise ValueError(
                f"Line {line_nbr + 1}: {[err['msg'] for err in e.errors()]}"
            )
        except ValueError as e:
            raise ValueError(f"Line {line_nbr + 1}: {e}")
        else:
            if config_dict["hub_type"] == "hub":
                hub = Hub(**config_dict)
            elif config_dict["hub_type"].startswith("start"):
                hub = StartHub(**config_dict)
            elif config_dict["hub_type"].startswith("end"):
                hub = EndHub(**config_dict)
            return hub

    def parse_connection(self, line: str, line_nbr: int) -> dict[str, Any]:
        pattern = (
            r"^(connection):"
            r"\s+([^\s\-]+)"
            r"-+([^\s\-]+)"
            r"(?:\s+\[(.*?)\])?$"
        )
        match = re.match(pattern, line)
        if not match:
            raise ValueError(f"Line {line_nbr + 1}: syntax error")

        _, hub1_name, hub2_name, max_link_capacity_str = match.groups()
        hubs_names = [hub.name for hub in self.hubs]
        if not (hub1_name in hubs_names and hub2_name in hubs_names):
            raise ValueError(f"Line {line_nbr + 1}: invalid hub name")
        else:
            hub1 = [hub for hub in self.hubs if hub.name == hub1_name][0]
            hub2 = [hub for hub in self.hubs if hub.name == hub2_name][0]

        max_link_capacity = 1
        if max_link_capacity_str:
            try:
                max_link_capacity = int(max_link_capacity_str.split("=")[1])
                if max_link_capacity <= 0:
                    raise ValueError(
                        "max_link_capacity must be a positive integer"
                    )
            except Exception as e:
                raise ValueError(f"Line {line_nbr + 1}: {e}")

        config_dict: dict[str, Any] = {
            "hub1": hub1,
            "hub2": hub2,
            "max_link_capacity": max_link_capacity,
        }
        return config_dict

    def get_connection(self, line: str, line_nbr: int) -> Connection:
        config_dict = self.parse_connection(line, line_nbr)
        start_node, end_node, max_link_capacity = [
            v for k, v in config_dict.items()
        ]
        return Connection(start_node, end_node, max_link_capacity)

    def parse_file(self) -> None:

        cleaned = self.get_cleaned_lines("config.txt")

        self.nb_drones = self.get_nb_drones(cleaned[0][1])
        self.hubs: list[Hub] = list()
        self.connections: list[Connection] = list()
        start_check, end_check = False, False

        for i in range(1, len(cleaned)):
            line_type: str = cleaned[i][1].split(":")[0]

            if "hub" in line_type:
                self.hubs.append(self.get_zone(cleaned[i][1], cleaned[i][0]))
                if line_type == "start_hub":
                    if int(self.hubs[-1].max_drones) < self.nb_drones:
                        raise ValueError("start_hub doesn't allow enough drones")
                    start_check = True
                elif line_type == "end_hub":
                    if int(self.hubs[-1].max_drones) < self.nb_drones:
                        raise ValueError("end_hub doesn't allow enough drones")
                    end_check = True
            elif "connection" == line_type:
                self.connections.append(
                    self.get_connection(cleaned[i][1], cleaned[i][0])
                )
            elif not line_type.startswith("#"):
                raise ValueError(f"Line {i + 1}: Syntax error")
        if not start_check or not end_check:
            raise ValueError("Needs both start_hub and end_hub")

        PatchBayValidator(self.connections).check_duplicates()

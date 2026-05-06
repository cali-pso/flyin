from typing import Any
from dataclasses import dataclass
from pydantic import BaseModel, model_validator  # type: ignore


class HubValidator(BaseModel):
    hub_type: str
    name: str
    x: int
    y: int
    zone: str | None = "normal"
    color: str | None = None
    max_drones: int | None = 1

    @model_validator(mode="after")
    def check_zone(self) -> Any:
        valid_zones = ["normal", "priority", "blocked", "restricted"]
        if self.zone and self.zone not in valid_zones:
            raise ValueError(f"Invalid zone {self.zone}")
        return self


@dataclass
class Hub:
    hub_type: str
    name: str
    x: int
    y: int
    zone: str = "normal"
    color: str = "purple"
    max_drones: int = 1


@dataclass
class StartHub(Hub):
    color: str = "blue"


@dataclass
class EndHub(Hub):
    color: str = "red"

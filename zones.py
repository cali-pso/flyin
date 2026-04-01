from typing import Any, Annotated
from pydantic import BaseModel, Field, model_validator


class ZoneValidator(BaseModel):
    hub_type: str
    name: str
    x: Annotated[int, Field(ge=0)]
    y: Annotated[int, Field(ge=0)]
    zone: str = "normal"
    color: str = None
    max_drones: Annotated[int, Field(ge=0, le=100)] = 1

    @model_validator(mode="after")
    def check_zone(self) -> Any:
        valid_types = ["normal", "priority", "blocked", "restricted"]
        if self.hub_type not in valid_types:
            raise ValueError(f"Invalid type {self.hub_type}")
        return self


class Hub:
    def __init__(
        self,
        x: int,
        y: int,
        zone: str = "normal",
        color: str = None,
        max_drones: int = 1,
    ):
        self.x = x
        self.y = y
        self.zone = zone
        self.color = color
        self.max_drones = max_drones


class StartHub(Hub):
    def __init__(
        self,
        x: int,
        y: int,
        zone: str = "normal",
        color: str = None,
        max_drones: int = 1,
    ):
        super().__init__(x, y, zone, color, max_drones)


class EndHub(Hub):
    def __init__(
        self,
        x: int,
        y: int,
        zone: str = "normal",
        color: str = None,
        max_drones: int = 1,
    ):
        super().__init__(x, y, zone, color, max_drones)

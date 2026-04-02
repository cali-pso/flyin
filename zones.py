from typing import Any, Annotated
from pydantic import BaseModel, Field, model_validator


class HubValidator(BaseModel):
    hub_type: str
    name: str
    x: Annotated[int, Field(ge=0)]
    y: Annotated[int, Field(ge=0)]
    zone: str | None = "normal"
    color: str | None = None
    max_drones: Annotated[int | None, Field(ge=0, le=100)] = 1

    @model_validator(mode="after")
    def check_zone(self) -> Any:
        valid_zones = ["normal", "priority", "blocked", "restricted"]
        if self.zone and self.zone not in valid_zones:
            raise ValueError(f"Invalid zone {self.zone}")
        return self


class Hub(BaseModel):
    hub_type: str
    name: str
    x: Annotated[int, Field(ge=0)]
    y: Annotated[int, Field(ge=0)]
    zone: str | None = "normal"
    color: str | None = None
    max_drones: Annotated[int | None, Field(ge=0, le=100)] = 1


class StartHub(Hub):
    pass


class EndHub(Hub):
    pass

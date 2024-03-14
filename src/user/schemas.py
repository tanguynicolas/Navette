# for pydantic models

from enum import Enum
from pydantic import BaseModel, EmailStr, PositiveInt

class VehicleColor(Enum):
    WHITE  = "white"
    BLACK  = "black"
    GREY   = "grey"
    BLUE   = "blue"
    RED    = "red"
    YELLOW = "yellow"
    ORANGE = "orange"

class User(BaseModel):
    id: PositiveInt
    email: EmailStr
    name: str
    verified: bool
    vehicle_model: str | None
    vehicle_color: VehicleColor | None
    vehicle_registration: str | None
    ticket_balance: PositiveInt = 0
    mac_beacon: str | None
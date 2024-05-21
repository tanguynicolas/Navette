# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, EmailStr, PositiveInt

from ..city.schemas import City
from ..zone.schemas import Zone
from ..stop.schemas import Stop

class UserList(BaseModel):
    id: PositiveInt
    email: EmailStr
    name: str

class UserBase(BaseModel):
    email: EmailStr
    name: str
    vehicle_model: Optional[str] = None
    vehicle_color: Optional[str] = None
    vehicle_registration: Optional[str] = None
    verified: Optional[bool] = False
    ticket_balance: Optional[int] = 0
    mac_beacon: Optional[str] = None

class UserCreate(UserBase):
    id_city: Optional[PositiveInt] = None
    id_zone: Optional[PositiveInt] = None
    id_stop: Optional[PositiveInt] = None

class UserUpdate(UserCreate):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    verified: Optional[bool] = None
    ticket_balance: Optional[int] = None

class User(UserBase):
    id: PositiveInt
    city: Optional[City] = None
    zone: Optional[Zone] = None
    stop: Optional[Stop] = None

    model_config = ConfigDict(
        from_attributes=True
    )

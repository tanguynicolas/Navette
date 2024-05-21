# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, EmailStr, PositiveInt

from ..city.schemas import CityList
from ..zone.schemas import ZoneList
from ..stop.schemas import StopList

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
    city: Optional[CityList] = None
    zone: Optional[ZoneList] = None
    stop: Optional[StopList] = None

    model_config = ConfigDict(
        from_attributes=True
    )

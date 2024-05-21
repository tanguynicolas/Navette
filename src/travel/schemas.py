# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from datetime import datetime
from typing import Optional, List

from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict, PositiveInt, EmailStr

class UserList(BaseModel):
    user_id: PositiveInt
    is_driver: bool

class TravelList(BaseModel):
    id: PositiveInt

class TravelBase(BaseModel):
    departure: PositiveInt
    arrival: PositiveInt
    back_travel: bool

class TravelCreate(TravelBase):
    driver_id: PositiveInt

class TravelUpdate(TravelCreate):
    departure: Optional[PositiveInt] = None
    arrival: Optional[PositiveInt] = None
    back_travel: Optional[bool] = None

class Travel(TravelBase):
    id: PositiveInt
    started_at: datetime
    finished_at: Optional[datetime] = None
    users: List[UserList]

    model_config = ConfigDict(
        from_attributes=True
    )

# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from datetime import datetime
from typing import Optional

from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict, PositiveInt

class TravelList(BaseModel):
    id: PositiveInt

class TravelBase(BaseModel):
    started_at: datetime
    finished_at: Optional[datetime] = None
    departure: str
    arrival: str
    back_travel: bool

class TravelCreate(TravelBase):
    driver_id: PositiveInt

class TravelUpdate(TravelCreate):
    started_at: Optional[datetime] = None
    departure: Optional[str] = None
    arrival: Optional[str] = None
    back_travel: Optional[bool] = None

class Travel(TravelBase):
    id: PositiveInt

    model_config = ConfigDict(
        from_attributes=True
    )

# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from typing import Optional
from datetime import time

from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict, PositiveInt

class StopList(BaseModel):
    id: PositiveInt
    name: str

class StopBase(BaseModel):
    name: str
    address: str
    picture: Optional[str] = None
    open_at: Optional[time] = None
    close_at: Optional[time] = None
    gps: Optional[str] = None

class StopCreate(StopBase):
    pass

class StopUpdate(StopCreate):
    name: Optional[str] = None
    address: Optional[str] = None

class Stop(StopBase):
    id: PositiveInt

    model_config = ConfigDict(
        from_attributes=True
    )

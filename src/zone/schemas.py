# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from typing import Optional

from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict

class ZoneList(BaseModel):
    id: int
    name: str

class ZoneBase(BaseModel):
    name: str
    description: Optional[str] = None
    picture: Optional[str] = None

class ZoneCreate(ZoneBase):
    pass

class ZoneUpdate(ZoneCreate):
    name: Optional[str] = None

class Zone(ZoneBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )

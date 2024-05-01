# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from typing import Optional, List

from typing_extensions import Annotated
from pydantic import BaseModel, Field, ConfigDict, EmailStr

from ..zone.schemas import ZoneList

"""
    Un modèle avec N attributs doit forcément être utilisé avec ses N attributs.
    La seule manière de l'utiliser sans spécifier tous les attributs, est de leur donner une valeur par défaut.

    a: str  # value required, None not allowed
    b: Optional[str]  # value required, None are allowed
    c: str = None  # value not required, but if it is provided it may not be None
    c2: OptionalDisallowNone[str] = None  # same as c but could satisfy mypy and friends
    d: Optional[str] = None  # value not required, if it is provided it may be None
"""

class CityList(BaseModel):
    id: int
    name: str

class CityBase(BaseModel):
    name: str

class CityCreate(CityBase):
    pass

class CityUpdate(CityCreate):
    name: Optional[str] = None

class City(CityBase):
    id: int
    zones: List[ZoneList] = []

    model_config = ConfigDict(
        from_attributes=True
    )

# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from pydantic import BaseModel # EmailStr, PositiveInt


class CityBase(BaseModel):
    name: str

# attributes needed for creation
class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    # used to provide configurations to Pydantic
    class Config:
        orm_mode = True

# for reading / returning
class UserBase(BaseModel):
    email: str
    name: str
    vehicle_model: str
    vehicle_color: str
    vehicle_registration: str
    mac_beacon: str

# attributes needed for creation
class UserCreate(UserBase):
    city_name: str

# for reading / returning
class User(UserBase):
    id: int
    verified: bool
    city: City
    #zone: Zone

    # used to provide configurations to Pydantic
    class Config:
        orm_mode = True

#class VehicleColor(Enum):
#    WHITE  = "white"
#    BLACK  = "black"
#    GREY   = "grey"
#    BLUE   = "blue"
#    RED    = "red"
#    YELLOW = "yellow"
#    ORANGE = "orange"
#
#class User(BaseModel):
#    id: PositiveInt
#    email: EmailStr
#    name: str
#    verified: bool
#    vehicle_model: str | None
#    vehicle_color: VehicleColor | None
#    vehicle_registration: str | None
#    ticket_balance: PositiveInt = 0
#    mac_beacon: str | None

# for pydantic models
# The data validation, conversion, and documentation classes and instances.
# « Resprésente comment moi j'ai envie d'envoyer ou de recevoir les données. »

from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    email: EmailStr

class UserAuthSuccess(UserAuth):
    id: int

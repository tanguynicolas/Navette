# is a core of each module with all the endpoints

from fastapi import APIRouter

from .schemas import User
from .models import users

router = APIRouter()

@router.get("/")
def get_users() -> list[User]:
    return(users)

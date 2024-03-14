# is a core of each module with all the endpoints

from fastapi import APIRouter

from .constants import debug
from .schemas import User
from .models import users

router = APIRouter()

@router.get("/debug")
def test():
    return(debug)

@router.get("/user")
def get_users() -> list[User]:
    return(users)




# ENDPOINTS GÉNÉRALISTES
# /user
# LIST
# 	Retourne la liste des utilisateurs.
# POST
# 	Ajoute un utilisateur.
# /user/{user}
# 	GET
# 		Retourne des informations sur un utilisateur spécifié.
# 	POST
# 		Met à jour un utilisateur spécifié.
# 	DELETE
# 		Supprime un utilisateur spécifié.
# 
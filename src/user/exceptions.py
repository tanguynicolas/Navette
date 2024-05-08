# module specific exceptions, e.g. PostNotFound, InvalidUserData

from fastapi import HTTPException

from .. import models

def check_user_id(id: int, user: models.User):
    if not user:
        raise HTTPException(status_code=404, detail=f"User identified by {id} not found")
    return

def check_user_email(user: models.User, exclude_id: int | None = None):
    if user:
        if exclude_id is None or user.id != exclude_id:
            raise HTTPException(status_code=409, detail=f"User {user.email} already registered")
    return

# Special usecase
def check_zone_id_only(id: int, zone: models.Zone):
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone identified by {id} not found")
    return

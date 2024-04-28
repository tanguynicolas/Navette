# module specific exceptions, e.g. PostNotFound, InvalidUserData

from fastapi import HTTPException

import models

def check_user_id(id: int, user: models.User):
    if not user:
        raise HTTPException(status_code=404, detail=f"User identified by {id} not found")
    return

def check_user_email(user: models.User, exclude_id: int | None = None):
    if user:
        if exclude_id is None or user.id != exclude_id:
            raise HTTPException(status_code=409, detail=f"User {user.email} already registered")
    return

def check_city_when_zone(zone_id: int | None, city_id: int | None):
    if zone_id and not city_id:
        raise HTTPException(status_code=400, detail="When zone_id is set, city_id is mandatory")
    return

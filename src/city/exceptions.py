# module specific exceptions, e.g. PostNotFound, InvalidUserData

from fastapi import HTTPException

from .. import models

def check_city_id(id: int, city: models.City):
    if not city:
        raise HTTPException(status_code=404, detail=f"City identified by {id} not found")
    return

def check_city_name(city: models.City, exclude_id: int | None = None):
    if city:
        if exclude_id is None or city.id != exclude_id:
            raise HTTPException(status_code=409, detail=f"City of {city.name} already registered")
    return

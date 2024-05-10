# module specific exceptions, e.g. PostNotFound, InvalidUserData

from fastapi import HTTPException

from .. import models

def check_stop_id(city_id: int, id: int, stop: models.Stop):
    if not stop:
        raise HTTPException(status_code=404, detail=f"Stop identified by {id} not found in city identified by {city_id}")
    return

def check_stop_name(city_id: int, stop: models.Stop, exclude_id: int | None = None):
    if stop:
        if exclude_id is None or stop.id != exclude_id:
            raise HTTPException(status_code=409, detail=f"Stop of {stop.name} already registered in city identified by {city_id}")
    return

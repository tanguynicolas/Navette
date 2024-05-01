# module specific exceptions, e.g. PostNotFound, InvalidUserData

from fastapi import HTTPException

from .. import models

def check_zone_id(city_id: int, id: int, zone: models.Zone):
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone identified by {id} not found in city identified by {city_id}")
    return

def check_zone_name(city_id: int, zone: models.Zone, exclude_id: int | None = None):
    if zone:
        if exclude_id is None or zone.id != exclude_id:
            raise HTTPException(status_code=409, detail=f"Zone of {zone.name} already registered in city identified by {city_id}")
    return

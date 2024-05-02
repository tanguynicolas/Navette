# is a core of each module with all the endpoints

from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import SessionLocal, engine
from .. import models
from . import service, schemas, exceptions
from ..city.service import select_city_by_id
from ..city.exceptions import check_city_id

models.Base.metadata.create_all(bind=engine) # To replace by Alembic

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.ZoneList])
def list_zones(city_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    return service.select_all_zones(db=db, city_id=city_id, skip=skip, limit=limit)

@router.get("/{zone_id}", response_model=schemas.Zone)
def read_zone(city_id: int, zone_id: int, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_zone = service.select_zone_by_id(db=db, city_id=city_id, id=zone_id)
    exceptions.check_zone_id(city_id=city_id, id=zone_id, zone=db_zone)
    return db_zone

@router.post("/", response_model=schemas.Zone)
def create_zone(city_id: int, zone: schemas.ZoneCreate, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_zone = service.select_zone_by_name(db=db, city_id=city_id, name=zone.name)
    exceptions.check_zone_name(city_id=city_id, zone=db_zone)
    return service.insert_zone(city_id=city_id, db=db, zone=zone)

@router.put("/{zone_id}", response_model=schemas.Zone)
def update_zone(city_id: int, zone_id: int, zone: schemas.ZoneUpdate, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_zone = service.select_zone_by_id(db=db, city_id=city_id, id=zone_id)
    exceptions.check_zone_id(city_id=city_id, id=zone_id, zone=db_zone)

    if zone.name:
        db_zone_test = service.select_zone_by_name(db=db, city_id=city_id, name=zone.name)
        exceptions.check_zone_name(city_id=city_id, zone=db_zone_test, exclude_id=zone_id)

    return service.update_zone(db=db, db_zone=db_zone, target_zone=zone)

@router.patch("/{zone_id}", response_model=schemas.Zone)
def partial_update_zone(city_id: int, zone_id: int, zone: schemas.ZoneUpdate, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_zone = service.select_zone_by_id(db=db, city_id=city_id, id=zone_id)
    exceptions.check_zone_id(city_id=city_id, id=zone_id, zone=db_zone)

    if zone.name:
        db_zone_test = service.select_zone_by_name(db=db, city_id=city_id, name=zone.name)
        exceptions.check_zone_name(city_id=city_id, zone=db_zone_test, exclude_id=zone_id)

    return service.partial_update_zone(db=db, db_zone=db_zone, target_zone=zone)

@router.delete("/{zone_id}", response_model=schemas.ZoneCreate)
def remove_zone(city_id: int, zone_id: int, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_zone = service.select_zone_by_id(db=db, city_id=city_id, id=zone_id)
    exceptions.check_zone_id(city_id=city_id, id=zone_id, zone=db_zone)
    return service.delete_zone(db=db, city_id=city_id, id=zone_id)

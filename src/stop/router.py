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

@router.get("/", response_model=List[schemas.StopList])
def list_stops(city_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    return service.select_all_stops(db=db, city_id=city_id, skip=skip, limit=limit)

@router.get("/{stop_id}", response_model=schemas.Stop)
def read_stop(city_id: int, stop_id: int, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_stop = service.select_stop_by_id(db=db, city_id=city_id, id=stop_id)
    exceptions.check_stop_id(city_id=city_id, id=stop_id, stop=db_stop)
    return db_stop

@router.post("/", response_model=schemas.Stop)
def create_stop(city_id: int, stop: schemas.StopCreate, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_stop = service.select_stop_by_name(db=db, city_id=city_id, name=stop.name)
    exceptions.check_stop_name(city_id=city_id, stop=db_stop)
    return service.insert_stop(city_id=city_id, db=db, stop=stop)

@router.put("/{stop_id}", response_model=schemas.Stop)
def update_stop(city_id: int, stop_id: int, stop: schemas.StopUpdate, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_stop = service.select_stop_by_id(db=db, city_id=city_id, id=stop_id)
    exceptions.check_stop_id(city_id=city_id, id=stop_id, stop=db_stop)

    if stop.name:
        db_stop_test = service.select_stop_by_name(db=db, city_id=city_id, name=stop.name)
        exceptions.check_stop_name(city_id=city_id, stop=db_stop_test, exclude_id=stop_id)

    return service.update_stop(db=db, db_stop=db_stop, target_stop=stop)

@router.patch("/{stop_id}", response_model=schemas.Stop)
def partial_update_stop(city_id: int, stop_id: int, stop: schemas.StopUpdate, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_stop = service.select_stop_by_id(db=db, city_id=city_id, id=stop_id)
    exceptions.check_stop_id(city_id=city_id, id=stop_id, stop=db_stop)

    if stop.name:
        db_stop_test = service.select_stop_by_name(db=db, city_id=city_id, name=stop.name)
        exceptions.check_stop_name(city_id=city_id, stop=db_stop_test, exclude_id=stop_id)

    return service.partial_update_stop(db=db, db_stop=db_stop, target_stop=stop)

@router.delete("/{stop_id}", response_model=schemas.StopCreate)
def remove_stop(city_id: int, stop_id: int, db: Session = Depends(get_db)):
    db_city = select_city_by_id(db=db, id=city_id)
    check_city_id(id=city_id, city=db_city)

    db_stop = service.select_stop_by_id(db=db, city_id=city_id, id=stop_id)
    exceptions.check_stop_id(city_id=city_id, id=stop_id, stop=db_stop)
    return service.delete_stop(db=db, city_id=city_id, id=stop_id)

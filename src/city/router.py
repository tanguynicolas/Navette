# is a core of each module with all the endpoints

from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import SessionLocal, engine
from .. import models
from . import service, schemas, exceptions

models.Base.metadata.create_all(bind=engine) # To replace by Alembic

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.CityList])
def list_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.select_all_cities(db=db, skip=skip, limit=limit)

@router.get("/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    db_city = service.select_city_by_id(db=db, id=city_id)
    exceptions.check_city_id(id=city_id, city=db_city)
    return db_city

@router.post("/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = service.select_city_by_name(db=db, name=city.name)
    exceptions.check_city_name(city=db_city)
    return service.insert_city(db=db, city=city)

@router.put("/{city_id}", response_model=schemas.City)
def update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = service.select_city_by_id(db=db, id=city_id)
    exceptions.check_city_id(id=city_id, city=db_city)

    if city.name:
        db_city_test = service.select_city_by_name(db=db, name=city.name)
        exceptions.check_city_name(city=db_city_test, exclude_id=city_id)

    return service.update_city(db=db, db_city=db_city, target_city=city)

@router.patch("/{city_id}", response_model=schemas.City)
def partial_update_city(city_id: int, city: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = service.select_city_by_id(db=db, id=city_id)
    exceptions.check_city_id(id=city_id, city=db_city)

    if city.name:
        db_city_test = service.select_city_by_name(db=db, name=city.name)
        exceptions.check_city_name(city=db_city_test, exclude_id=city_id)

    return service.partial_update_city(db=db, db_city=db_city, target_city=city)

@router.delete("/{city_id}", response_model=schemas.CityCreate)
def remove_city(city_id: int, db: Session = Depends(get_db)):
    db_city = service.select_city_by_id(db=db, id=city_id)
    exceptions.check_city_id(id=city_id, city=db_city)
    return service.delete_city(db=db, id=city_id)

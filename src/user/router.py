# is a core of each module with all the endpoints

from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import EmailStr

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

@router.get("/", response_model=List[schemas.UserList])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.select_all_users(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.select_user_by_id(db=db, id=user_id)
    exceptions.check_user_id(id=user_id, user=db_user)
    return db_user

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.select_user_by_email(db=db, email=user.email)
    exceptions.check_user_email(user=db_user)

    if user.id_city:
        db_city = select_city_by_id(db=db, id=user.id_city)
        check_city_id(id=user.id_city, city=db_city)
    if user.id_zone:
        db_zone = service.select_zone_by_id_only(db=db, id=user.id_zone)
        exceptions.check_zone_id_only(id=user.id_zone, zone=db_zone)

    return service.insert_user(db=db, user=user)

@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = service.select_user_by_id(db=db, id=user_id)
    exceptions.check_user_id(id=user_id, user=db_user)

    if user.email:
        db_user_test = service.select_user_by_email(db=db, email=user.email)
        exceptions.check_user_email(user=db_user_test, exclude_id=user_id)

    if user.id_city:
        db_city = select_city_by_id(db=db, id=user.id_city)
        check_city_id(id=user.id_city, city=db_city)
    if user.id_zone:
        db_zone = service.select_zone_by_id_only(db=db, id=user.id_zone)
        exceptions.check_zone_id_only(id=user.id_zone, zone=db_zone)

    return service.update_user(db=db, db_user=db_user, target_user=user)

@router.patch("/{user_id}", response_model=schemas.User)
def partial_update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = service.select_user_by_id(db=db, id=user_id)
    exceptions.check_user_id(id=user_id, user=db_user)

    if user.email:
        db_user_test = service.select_user_by_email(db=db, email=user.email)
        exceptions.check_user_email(user=db_user_test, exclude_id=user_id)

    if user.id_city:
        db_city = select_city_by_id(db=db, id=user.id_city)
        check_city_id(id=user.id_city, city=db_city)
    if user.id_zone:
        db_zone = service.select_zone_by_id_only(db=db, id=user.id_zone)
        exceptions.check_zone_id_only(id=user.id_zone, zone=db_zone)

    return service.partial_update_user(db=db, db_user=db_user, target_user=user)

@router.delete("/{user_id}", response_model=schemas.UserCreate)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.select_user_by_id(db=db, id=user_id)
    exceptions.check_user_id(id=user_id, user=db_user)
    return service.delete_user(db=db, id=user_id)

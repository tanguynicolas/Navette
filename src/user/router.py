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
from ..travel.schemas import TravelHistory

models.Base.metadata.create_all(bind=engine)

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
    if user.id_stop:
        db_stop = service.select_stop_by_id_only(db=db, id=user.id_stop)
        exceptions.check_stop_id_only(id=user.id_stop, stop=db_stop)

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
    if user.id_stop:
        db_stop = service.select_stop_by_id_only(db=db, id=user.id_stop)
        exceptions.check_stop_id_only(id=user.id_stop, stop=db_stop)

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
    if user.id_stop:
        db_stop = service.select_stop_by_id_only(db=db, id=user.id_stop)
        exceptions.check_stop_id_only(id=user.id_stop, stop=db_stop)

    return service.partial_update_user(db=db, db_user=db_user, target_user=user)

@router.delete("/{user_id}", response_model=schemas.UserCreate)
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.select_user_by_id(db=db, id=user_id)
    exceptions.check_user_id(id=user_id, user=db_user)
    return service.delete_user(db=db, id=user_id)


# Special endpoints

from typing import List

from fastapi import HTTPException

@router.get("/{user_id}/history", response_model=List[TravelHistory])
def get_user_travel_history(
    user_id: int,
    back_travel: bool = True,
    outgoing_travel: bool = True,
    is_finished: bool | None = None,
    db: Session = Depends(get_db)
):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = db.query(models.Travel, models.UserTravel.is_driver).join(models.UserTravel).filter(models.UserTravel.user_id == user_id)

    if back_travel and outgoing_travel:
        query = query.filter(models.Travel.back_travel.in_([True, False]))
    elif back_travel:
        query = query.filter(models.Travel.back_travel == True)
    elif outgoing_travel:
        query = query.filter(models.Travel.back_travel == False)
    else:
        return []

    if is_finished is not None:
        if is_finished:
            query = query.filter(models.Travel.finished_at != None)
        else:
            query = query.filter(models.Travel.finished_at == None)

    results = query.all()
    travels = [TravelHistory(
        id=travel.id,
        started_at=travel.started_at,
        finished_at=travel.finished_at,
        departure=travel.departure,
        arrival=travel.arrival,
        back_travel=travel.back_travel,
        is_driver=is_driver
    ) for travel, is_driver in results]
    return travels

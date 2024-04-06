# is a core of each module with all the endpoints

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import service, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine) # To replace by Alembic

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
    USERS routes
"""

@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.check_existing_user(db, user)
    if db_user:
        raise HTTPException(status_code=409, detail="One of the unique attribute already registered")
    return service.create_user(db=db, user=user)

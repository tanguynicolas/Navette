# is a core of each module with all the endpoints

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from . import schemas, exceptions
from user.service import select_user_by_email

models.Base.metadata.create_all(bind=engine) # To replace by Alembic

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserAuthSuccess)
def authenticate(user: schemas.UserAuth, db: Session = Depends(get_db)):
    db_user = select_user_by_email(db=db, email=user.email)
    exceptions.check_user_email(email=user.email, user=db_user)
    return db_user

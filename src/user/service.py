# module specific business logic
# « Rend possible l'utilisation désirée (schemas) avec l'utilisation réelle (models). »

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from pydantic import EmailStr

from .. import models
from . import schemas

def select_all_users(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(select(models.User.id, models.User.name, models.User.email).offset(skip).limit(limit)).fetchall()
    return [{"id": row[0], "name": row[1], "email": row[2]} for row in result]

def select_user_by_id(db: Session, id: int):
    return db.get(models.User, id)

def select_user_by_email(db: Session, email: EmailStr):
    return db.scalar(select(models.User).where(models.User.email == email))

def insert_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        name=user.name,
        vehicle_model=user.vehicle_model,
        vehicle_color=user.vehicle_color,
        vehicle_registration=user.vehicle_registration,
        verified=user.verified,
        ticket_balance=user.ticket_balance,
        mac_beacon=user.mac_beacon,
        id_city=user.id_city,
        id_zone=user.id_zone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: models.User, target_user: schemas.UserUpdate):
    # db_user is tracked
    
    # Code moche mais je n'ai pas trouvé mieux...
    exclusions = set()
    if target_user.name is None:
        exclusions.add('name')
    if target_user.email is None:
        exclusions.add('email')
    if target_user.verified is None:
        target_user.verified = False
    if target_user.ticket_balance is None:
        target_user.ticket_balance = 0

    target_user_refactored = target_user.model_dump(exclude=exclusions).items()

    for attr, value in target_user_refactored:
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def partial_update_user(db: Session, db_user: models.User, target_user: schemas.UserUpdate):
    for attr, value in target_user.model_dump(exclude_unset=True).items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: int):
    db_user = db.get(models.User, id)
    db.delete(db_user)
    db.commit()
    return db_user

# Special usecase
def select_zone_by_id_only(db: Session, id: int):
    return db.get(models.Zone, id)

# module specific business logic
# « Rend possible l'utilisation désirée (schemas) avec l'utilisation réelle (models). »

from sqlalchemy.orm import Session

from . import models, schemas


"""
    CITIES functions
"""

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name)
    db.add(db_city)
    db.commit()

    db.refresh(db_city)
    return db_city

"""
    USERS functions
"""

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_city = get_city_by_name(db, user.city_name)
    if not db_city:
        city = schemas.CityCreate(name=user.city_name)
        db_city = create_city(db, city)

    db_user = models.User(
        email = user.email,
        name = user.name,
        vehicle_model = user.vehicle_model,
        vehicle_color = user.vehicle_color,
        vehicle_registration = user.vehicle_registration,
        mac_beacon = user.mac_beacon,
        city=db_city
    )
    db.add(db_user)
    db.commit()

    db.refresh(db_user)
    db.refresh(db_user.city)
    return db_user

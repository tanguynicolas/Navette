# module specific business logic
# « Rend possible l'utilisation désirée (schemas) avec l'utilisation réelle (models). »

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from .. import models
from . import schemas


def select_all_stops(db: Session, city_id: int, skip: int = 0, limit: int = 100):
    result = db.execute(select(models.Stop.id, models.Stop.name).where(models.Stop.id_city == city_id).offset(skip).limit(limit)).fetchall()
    return [{"id": row[0], "name": row[1]} for row in result]

def select_stop_by_id(db: Session, city_id: int, id: int):
    return db.scalar(select(models.Stop).where(models.Stop.id_city == city_id).where(models.Stop.id == id))

def select_stop_by_name(db: Session, city_id: int, name: str):
    return db.scalar(select(models.Stop).where(models.Stop.id_city == city_id).where(models.Stop.name == name))

def insert_stop(db: Session, city_id: int, stop: schemas.StopCreate):
    db_stop = models.Stop(name=stop.name,
                          address=stop.address,
                          picture=stop.picture,
                          open_at=stop.open_at,
                          close_at=stop.close_at,
                          gps=stop.gps,
                          in_wait=0,
                          id_city=city_id)
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop

def update_stop(db: Session, db_stop: models.Stop, target_stop: schemas.StopUpdate):
    # db_stop is tracked
    
    # Code moche mais je n'ai pas trouvé mieux...
    exclusions = set()
    if target_stop.name is None:
        exclusions.add('name')
    if target_stop.address is None:
        exclusions.add('address')

    target_stop_refactored = target_stop.model_dump(exclude=exclusions).items()

    for attr, value in target_stop_refactored:
        setattr(db_stop, attr, value)
    db.commit()
    db.refresh(db_stop)
    return db_stop

def partial_update_stop(db: Session, db_stop: models.Stop, target_stop: schemas.StopUpdate):
    for attr, value in target_stop.model_dump(exclude_unset=True).items():
        setattr(db_stop, attr, value)
    db.commit()
    db.refresh(db_stop)
    return db_stop

def delete_stop(db: Session, city_id: int, id: int):
    db_stop = db.scalar(select(models.Stop).where(models.Stop.id_city == city_id).where(models.Stop.id == id))
    db.delete(db_stop)
    db.commit()
    return db_stop

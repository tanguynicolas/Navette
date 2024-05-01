# module specific business logic
# « Rend possible l'utilisation désirée (schemas) avec l'utilisation réelle (models). »

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from .. import models
from . import schemas


def select_all_zones(db: Session, city_id: int, skip: int = 0, limit: int = 100):
    result = db.execute(select(models.Zone.id, models.Zone.name).where(models.Zone.id_city == city_id).offset(skip).limit(limit)).fetchall()
    return [{"id": row[0], "name": row[1]} for row in result]

def select_zone_by_id(db: Session, city_id: int, id: int):
    return db.scalar(select(models.Zone).where(models.Zone.id_city == city_id).where(models.Zone.id == id))

def select_zone_by_name(db: Session, city_id: int, name: str):
    return db.scalar(select(models.Zone).where(models.Zone.id_city == city_id).where(models.Zone.name == name))

def insert_zone(db: Session, city_id: int, zone: schemas.ZoneCreate):
    db_zone = models.Zone(name=zone.name,
                          description=zone.description,
                          picture=zone.picture,
                          id_city=city_id)
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def update_zone(db: Session, db_zone: models.Zone, target_zone: schemas.ZoneUpdate):
    # db_zone is tracked
    
    # Code moche mais je n'ai pas trouvé mieux...
    target_zone_refactored = target_zone.model_dump().items()
    if target_zone.name is None:
        target_zone_refactored = target_zone.model_dump(exclude={'name'}).items()

    for attr, value in target_zone_refactored:
        setattr(db_zone, attr, value)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def partial_update_zone(db: Session, db_zone: models.Zone, target_zone: schemas.ZoneUpdate):
    for attr, value in target_zone.model_dump(exclude_unset=True).items():
        setattr(db_zone, attr, value)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def delete_zone(db: Session, city_id: int, id: int):
    db_zone = db.scalar(select(models.Zone).where(models.Zone.id_city == city_id).where(models.Zone.id == id))
    db.delete(db_zone)
    db.commit()
    return db_zone

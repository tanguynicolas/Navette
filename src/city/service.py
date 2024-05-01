# module specific business logic
# « Rend possible l'utilisation désirée (schemas) avec l'utilisation réelle (models). »

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from .. import models
from . import schemas


def select_all_cities(db: Session, skip: int = 0, limit: int = 100):
    result = db.execute(select(models.City.id, models.City.name).offset(skip).limit(limit)).fetchall()
    return [{"id": row[0], "name": row[1]} for row in result]

def select_city_by_id(db: Session, id: int):
    return db.get(models.City, id)

def select_city_by_name(db: Session, name: str):
    return db.scalar(select(models.City).where(models.City.name == name))

def insert_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city.name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, db_city: models.City, target_city: schemas.CityUpdate):
    # db_city is tracked
    
    # NOTE: Le problème actuel est que je suis obligé de passer le nom exact de la city si je ne souhaite pas le modifier
    # Car c'est un attribut non-nullable => si je ne passe pas le nom, j'aurais une erreur.
    # Je voudrais plutôt que, si je ne passe pas le nom, étant donné la nature non-nullable de l'attribut,
    # le nom ne soit simplement pas modifié.
    # NOTE: Pas le choix, il faut mettre une valeur par défaut dans l'attribut de schéma
    # Ensuite il faudra supprimer l'attribut que l'on ne souhaite pas modifier (genre name), via un code Python spécifique
    # Il existe peut-être une méthode sur l'objet du modèle pour supprimet un attribut.
    # SINON
    # Creuser la piste des labels. L'idée c'est de labelisé les champs comme name que l'on ne souhaite pas modifier
    # Et ensuite via une méthode d'objet Pydantic, agir sur tous les labels (suppression par exemple)

    # Code moche mais je n'ai pas trouvé mieux...
    target_city_refactored = target_city.model_dump().items()
    if target_city.name is None:
        target_city_refactored = target_city.model_dump(exclude={'name'}).items()

    for attr, value in target_city_refactored:
        setattr(db_city, attr, value)
    db.commit()
    db.refresh(db_city)
    return db_city

def partial_update_city(db: Session, db_city: models.City, target_city: schemas.CityUpdate):
    for attr, value in target_city.model_dump(exclude_unset=True).items():
        setattr(db_city, attr, value)
    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, id: int):
    db_city = db.get(models.City, id)
    db.delete(db_city)
    db.commit()
    return db_city

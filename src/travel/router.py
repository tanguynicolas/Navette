# is a core of each module with all the endpoints

from typing import List
from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.future import select

from ..database import SessionLocal, engine
from .. import models
from . import service, schemas, exceptions

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.TravelList])
def list_travels(
        back_travel: bool = True,
        outgoing_travel: bool = True,
        is_finished: bool | None = None,
        db: Session = Depends(get_db)
    ):
    query = db.query(models.Travel)

    # Gérer les filtres pour les trajets allés et retours
    if back_travel and outgoing_travel:
        query = query.filter(models.Travel.back_travel.in_([True, False]))  # N'inclut rien de plus puisque c'est tous les trajets
    elif back_travel:
        query = query.filter(models.Travel.back_travel == True)
    elif outgoing_travel:
        query = query.filter(models.Travel.back_travel == False)
    else:
        return []
    
    # Gérer les filtres pour les trajets terminés ou en cours
    if is_finished is not None:
        if is_finished:
            query = query.filter(models.Travel.finished_at != None)
        else:
            query = query.filter(models.Travel.finished_at == None)

    travels = query.all()
    return travels

@router.get("/{travel_id}", response_model=schemas.Travel)
def read_travel(travel_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(models.Travel)
        .options(selectinload(models.Travel.users).selectinload(models.UserTravel.user))
        .where(models.Travel.id == travel_id)
    )
    result = db.execute(stmt)
    db_travel = result.scalars().first()
    if db_travel is None:
        raise HTTPException(status_code=404, detail="Travel not found")
    
    return db_travel

@router.post("/", response_model=schemas.Travel)
def create_travel(travel: schemas.TravelCreate, db: Session = Depends(get_db)):
    # Vérifiez si l'utilisateur (conducteur) existe
    driver = db.get(models.User, travel.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    # Créez le trajet
    new_travel = models.Travel(
        started_at=datetime.now(),
        departure=travel.departure,
        arrival=travel.arrival,
        back_travel=travel.back_travel
    )
    db.add(new_travel)
    db.flush()  # Flush pour récupérer l'ID avant de commettre la transaction

    # Associez le conducteur au trajet
    driver_association = models.UserTravel(
        user_id=travel.driver_id,
        travel_id=new_travel.id,
        is_driver=True
    )
    db.add(driver_association)
    db.commit()

    return new_travel

@router.post("/{travel_id}/add-user/{user_id}", response_model=schemas.Travel)
def add_user_to_travel(travel_id: int, user_id: int, db: Session = Depends(get_db)):
    # Vérifiez si le trajet existe
    travel = db.get(models.Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")

    # Vérifiez si l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Créez une nouvelle association UserTravel sans marquer l'utilisateur comme conducteur
    user_travel = models.UserTravel(user_id=user_id, travel_id=travel_id, is_driver=False)
    db.add(user_travel)
    db.commit()
    db.refresh(user_travel)

    return travel

@router.delete("/{travel_id}/remove-user/{user_id}", response_model=schemas.Travel)
def remove_user_from_travel(travel_id: int, user_id: int, db: Session = Depends(get_db)):
    travel = db.get(models.Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")

    # Vérifiez si l'utilisateur existe
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Trouvez l'association et retirez-la
    user_travel = db.query(models.UserTravel).filter(
        models.UserTravel.travel_id == travel_id,
        models.UserTravel.user_id == user_id
    ).first()
    if not user_travel:
        raise HTTPException(status_code=404, detail="Association not found")
    db.delete(user_travel)
    db.commit()

    return travel

@router.patch("/{travel_id}/finish", response_model=schemas.Travel)
def finish_travel(travel_id: int, db: Session = Depends(get_db)):
    # Trouvez le trajet en utilisant l'ID fourni
    travel = db.get(models.Travel, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")
    
    # Vérifiez si le trajet n'est pas déjà terminé
    if travel.finished_at is not None:
        raise HTTPException(status_code=400, detail="Travel is already finished")

    # Mettre à jour le champ finished_at avec la date et l'heure actuelles
    travel.finished_at = datetime.now()
    db.commit()
    db.refresh(travel)

    return travel

# is a core of each module with all the endpoints

from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

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

@router.post("/", response_model=schemas.Travel)
def create_travel(travel: schemas.TravelCreate, db: Session = Depends(get_db)):
    # Vérifiez si l'utilisateur (conducteur) existe
    driver = db.get(models.User, travel.driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")

    # Créez le trajet
    new_travel = models.Travel(
        started_at=travel.started_at,
        finished_at=travel.finished_at,
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

@router.post("{travel_id}/add-user/{user_id}")
def add_user_to_travel(travel_id: int, user_id: int, db: Session = Depends(get_db)):
    # Vérifiez si le trajet existe
    travel = db.query(models.Travel).filter(models.Travel.id == travel_id).first()
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

    return {"message": "User added to travel successfully"}

@router.delete("{travel_id}/remove-user/{user_id}")
def remove_user_from_travel(travel_id: int, user_id: int, db: Session = Depends(get_db)):
    # Trouvez l'association et retirez-la
    user_travel = db.query(models.UserTravel).filter(
        models.UserTravel.travel_id == travel_id,
        models.UserTravel.user_id == user_id
    ).first()
    if not user_travel:
        raise HTTPException(status_code=404, detail="Association not found")

    db.delete(user_travel)
    db.commit()

    return {"message": "User removed from travel successfully"}

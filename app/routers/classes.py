from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud
from ..utils import raise_400, raise_404

router = APIRouter(prefix="/classes", tags=["classes"])

@router.post("", response_model=schemas.ClassOut, status_code=201)
def create_class(payload: schemas.ClassCreate, db: Session = Depends(get_db)):
    if crud.get_class_by_number(db, payload.number):
        raise_400("Ce numéro de classe existe déjà")
    return crud.create_class(db, payload)

@router.get("", response_model=list[schemas.ClassOut])
def list_classes(db: Session = Depends(get_db)):
    return crud.list_classes(db)

@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(class_id: int, db: Session = Depends(get_db)):
    cls = crud.get_class_by_id(db, class_id)
    if not cls:
        raise_404("Classe introuvable")
    return cls

@router.get("/by-number/{number}", response_model=schemas.ClassOut)
def get_class_by_number(number: str, db: Session = Depends(get_db)):
    cls = crud.get_class_by_number(db, number)
    if not cls:
        raise_404("Classe introuvable")
    return cls
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from .. import schemas, crud
from ..utils import raise_400, raise_404

router = APIRouter(prefix="/schedules", tags=["schedules"])

@router.post("/class/{class_id}", response_model=schemas.ScheduleOut, status_code=201)
def add_schedule_entry(class_id: int, payload: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    if not crud.get_class_by_id(db, class_id):
        raise_404("Classe introuvable")
    try:
        return crud.create_schedule_entry(db, class_id, payload)
    except ValueError as e:
        raise_400(str(e))

@router.get("/class/{class_id}", response_model=list[schemas.ScheduleOut])
def get_schedule_for_class(
    class_id: int,
    start: datetime | None = Query(None, description="Filtrer à partir de cette date/heure"),
    end: datetime | None = Query(None, description="Filtrer jusqu'à cette date/heure"),
    db: Session = Depends(get_db),
):
    if not crud.get_class_by_id(db, class_id):
        raise_404("Classe introuvable")
    return crud.list_schedule_for_class(db, class_id, start, end)

@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_schedule_entry(db, entry_id)
    if not ok:
        raise_404("Entrée introuvable")
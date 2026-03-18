from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime
from . import models, schemas

# ---- Classes ----
def create_class(db: Session, data: schemas.ClassCreate) -> models.Class:
    obj = models.Class(number=data.number, name=data.name, level=data.level)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_class_by_id(db: Session, class_id: int) -> models.Class | None:
    return db.get(models.Class, class_id)

def get_class_by_number(db: Session, number: str) -> models.Class | None:
    return db.scalar(select(models.Class).where(models.Class.number == number))

def list_classes(db: Session) -> list[models.Class]:
    return list(db.scalars(select(models.Class).order_by(models.Class.number)).all())

# ---- Schedules ----
def timeslot_overlaps(db: Session, class_id: int, start: datetime, end: datetime) -> bool:
    # Overlap if existing.start < new_end AND existing.end > new_start
    stmt = select(models.ScheduleEntry).where(
        and_(
            models.ScheduleEntry.class_id == class_id,
            models.ScheduleEntry.start_time < end,
            models.ScheduleEntry.end_time > start,
        )
    )
    return db.scalars(stmt).first() is not None

def create_schedule_entry(db: Session, class_id: int, data: schemas.ScheduleCreate) -> models.ScheduleEntry:
    if data.end_time <= data.start_time:
        raise ValueError("end_time doit être > start_time")

    if timeslot_overlaps(db, class_id, data.start_time, data.end_time):
        raise ValueError("Le créneau se chevauche avec un autre pour cette classe")

    entry = models.ScheduleEntry(
        class_id=class_id,
        subject=data.subject,
        teacher=data.teacher,
        room=data.room,
        start_time=data.start_time,
        end_time=data.end_time,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def list_schedule_for_class(db: Session, class_id: int, start: datetime | None, end: datetime | None):
    stmt = select(models.ScheduleEntry).where(models.ScheduleEntry.class_id == class_id)
    if start:
        stmt = stmt.where(models.ScheduleEntry.end_time >= start)
    if end:
        stmt = stmt.where(models.ScheduleEntry.start_time <= end)
    stmt = stmt.order_by(models.ScheduleEntry.start_time)
    return list(db.scalars(stmt).all())

def delete_schedule_entry(db: Session, entry_id: int) -> bool:
    obj = db.get(models.ScheduleEntry, entry_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
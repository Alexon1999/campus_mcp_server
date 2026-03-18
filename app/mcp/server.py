from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Class, ScheduleEntry
from datetime import datetime

router = APIRouter()

def mcp_response(data):
    return {"content": [{"type": "text", "text": str(data)}]}

@router.post("/list_classes")
def list_classes(db: Session = Depends(get_db)):
    cls = db.query(Class).all()
    return mcp_response([{"id": c.id, "number": c.number} for c in cls])

@router.post("/get_class_by_number")
def get_class(body: dict, db: Session = Depends(get_db)):
    number = body["arguments"]["number"]
    c = db.query(Class).filter(Class.number == number).first()
    return mcp_response(c.__dict__ if c else "Not found")

@router.post("/add_schedule_entry")
def add_entry(body: dict, db: Session = Depends(get_db)):
    args = body["arguments"]
    entry = ScheduleEntry(
        class_id=args["class_id"],
        subject=args["subject"],
        start_time=datetime.fromisoformat(args["start_time"]),
        end_time=datetime.fromisoformat(args["end_time"]),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return mcp_response(f"Saved entry {entry.id}")

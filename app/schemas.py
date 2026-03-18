from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ClassBase(BaseModel):
    number: str = Field(..., description="Numéro unique de la classe, ex: 6A")
    name: str = Field(..., description="Nom affiché, ex: Sixième A")
    level: str | None = Field(None, description="Niveau, ex: 6e, 5e, etc.")

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ScheduleCreate(BaseModel):
    subject: str
    teacher: str | None = None
    room: str | None = None
    start_time: datetime
    end_time: datetime

class ScheduleOut(ScheduleCreate):
    id: int
    class_id: int
    model_config = ConfigDict(from_attributes=True)
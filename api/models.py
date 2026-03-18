from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .database import Base

class Class(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # numéro de classe unique
    name: Mapped[str] = mapped_column(String(100))
    level: Mapped[str | None] = mapped_column(String(50), nullable=True)

    schedules = relationship("ScheduleEntry", back_populates="clazz", cascade="all, delete-orphan")


class ScheduleEntry(Base):
    __tablename__ = "schedule_entries"
    __table_args__ = (
        UniqueConstraint("class_id", "start_time", "end_time", "room", name="uq_class_time_room"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), index=True)
    subject: Mapped[str] = mapped_column(String(100))
    teacher: Mapped[str | None] = mapped_column(String(100), nullable=True)
    room: Mapped[str | None] = mapped_column(String(50), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    clazz = relationship("Class", back_populates="schedules")
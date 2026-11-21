from database import Base

from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, Text, Boolean, DateTime

from datetime import datetime, timezone

def utc_now_native():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class Task(Base):
    __tablename__ = "tasks"
    
    id = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    title = mapped_column(
        Text,
        nullable=False
    )
    
    description = mapped_column(
        Text,
        nullable=True,
        default=None
    )
    
    is_completed = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    
    created_at = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=utc_now_native
    )
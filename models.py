from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from database import Base
from datetime import datetime
from typing import Optional, Dict, Any

# SQLAlchemy Model (Database Table)
class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    sender = Column(String, index=True)
    message = Column(String)
    chat_type = Column(String)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    status = Column(String, default="todo")
    parent_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    attributes = Column(JSON, default={})

    children = relationship("Task", backref="parent", remote_side=[id])

class GameEvent(Base):
    __tablename__ = "game_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    event_type = Column(String, index=True)
    payload = Column(JSON)

# Pydantic Model (API Schema)
class ChatMessageCreate(BaseModel):
    sender: str
    message: str
    chat_type: str

class GameEventCreate(BaseModel):
    event_type: str
    payload: Dict[str, Any]

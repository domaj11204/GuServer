from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ChatLog, ChatMessageCreate, GameEvent, GameEventCreate

router = APIRouter(prefix="/ffxiv", tags=["ffxiv"])

@router.post("/chat")
def receive_chat(chat_data: ChatMessageCreate, db: Session = Depends(get_db)):
    print(f"Received Chat: [{chat_data.chat_type}] {chat_data.sender}: {chat_data.message}")
    
    # Save to DB
    db_chat = ChatLog(
        sender=chat_data.sender, 
        message=chat_data.message, 
        chat_type=chat_data.chat_type
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    return {"status": "success", "id": db_chat.id}

@router.post("/event")
def receive_event(event_data: GameEventCreate, db: Session = Depends(get_db)):
    print(f"Received Event: [{event_data.event_type}] {event_data.payload}")
    
    db_event = GameEvent(
        event_type=event_data.event_type,
        payload=event_data.payload
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return {"status": "success", "id": db_event.id}

@router.get("/chat")
def get_chat_logs(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(ChatLog).order_by(ChatLog.timestamp.desc()).limit(limit).all()

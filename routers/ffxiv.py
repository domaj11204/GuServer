from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ChatLog, ChatMessageCreate

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

@router.get("/chat")
def get_chat_logs(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(ChatLog).order_by(ChatLog.timestamp.desc()).limit(limit).all()

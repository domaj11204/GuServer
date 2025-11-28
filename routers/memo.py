from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

router = APIRouter(prefix="/memo", tags=["memo"])

# Pydantic Models for Task
class TaskCreate(BaseModel):
    title: str
    status: str = "todo"
    parent_id: Optional[int] = None
    attributes: Dict[str, Any] = {}

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    attributes: Dict[str, Any]

    class Config:
        from_attributes = True

# CRUD Endpoints

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        status=task.status,
        parent_id=task.parent_id,
        attributes=task.attributes
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    return query.all()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"ok": True}

@router.get("/context")
def get_context(db: Session = Depends(get_db)):
    """
    Generates a markdown summary of the current context.
    Useful for AI to quickly grasp what's going on.
    """
    active_tasks = db.query(Task).filter(Task.status == "in_progress").all()
    todo_tasks = db.query(Task).filter(Task.status == "todo").limit(5).all()
    
    md = "# Current Context\n\n"
    
    md += "## Active Tasks\n"
    if not active_tasks:
        md += "*No active tasks.*\n"
    for task in active_tasks:
        md += f"- **{task.title}** (ID: {task.id})\n"
        if task.attributes:
            md += f"  - Attributes: {task.attributes}\n"
            
    md += "\n## Up Next\n"
    for task in todo_tasks:
        md += f"- {task.title} (ID: {task.id})\n"
        
    return {"markdown": md}

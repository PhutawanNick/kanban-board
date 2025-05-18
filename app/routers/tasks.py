from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Task  
from ..schemas.tasks import Task as TaskSchema, TaskCreate, TaskUpdate
from .. import oauth2

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=List[TaskSchema])
def get_tasks(db: Session = Depends(get_db), 
              current_user: User = Depends(oauth2.get_current_user)):
    tasks = db.query(Task).all()
    return tasks

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
def create_task(task: TaskCreate, 
                db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{task_id}", response_model=TaskSchema)
def get_task(task_id: int, 
             db: Session = Depends(get_db),
             current_user: User = Depends(oauth2.get_current_user)):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskSchema)
def update_task(task_id: int, 
                task: TaskUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    task_query = db.query(Task).filter(Task.task_id == task_id)
    if not task_query.first():
        raise HTTPException(status_code=404, detail="Task not found")
    task_query.update(task.dict())
    db.commit()
    return task_query.first()

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, 
                db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    task = db.query(Task).filter(Task.task_id == task_id)
    if not task.first():
        raise HTTPException(status_code=404, detail="Task not found")
    task.delete()
    db.commit()
    return None

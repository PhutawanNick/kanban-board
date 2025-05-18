from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, oauth2
from ..schemas.users import UserOut, UserUpdate  
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, 
             db: Session = Depends(get_db),
             current_user: models.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int,
                user_update: UserUpdate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # Check if user is updating their own profile
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
        
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    if not user_query.first():
        raise HTTPException(status_code=404, detail="User not found")
        
    user_query.update(user_update.dict(exclude_unset=True))
    db.commit()
    return user_query.first()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # Check if user is deleting their own account
    if user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
        
    user = db.query(models.User).filter(models.User.user_id == user_id)
    if not user.first():
        raise HTTPException(status_code=404, detail="User not found")
        
    user.delete()
    db.commit()
    return None
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, utils, oauth2
from ..schemas.users import UserCreate, UserOut, Token  
from ..database import get_db

router = APIRouter(
    tags=['Authentication']
)

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    # Create user
    new_user = models.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        raise HTTPException(status_code=400, 
                          detail="Username or email already exists")
    return new_user

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=403, 
                          detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password_hash):
        raise HTTPException(status_code=403,
                          detail="Invalid credentials")
    
    # Create token
    access_token = oauth2.create_access_token(data={"user_id": user.user_id})
    
    return {"access_token": access_token, "token_type": "bearer"}
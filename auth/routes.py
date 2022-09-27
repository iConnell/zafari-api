from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schemas, models
from .database import get_db
from .utils import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix='/api/auth', 
    tags=['Authentication']
    )


@router.post('', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email==user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {user.email} already exist")
    
    hashed_password = hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"token":create_access_token({"email": new_user.email, "id":new_user.id})}


@router.post('/login', status_code=status.HTTP_200_OK)
def user_login(credentials: schemas.UserCreate, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==credentials.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials provied")
    
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials provied")

    return {"token":create_access_token({"email": user.email, "id":user.id})}
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..utils import get_current_user, verify_access_token, hash_password, verify_password, create_access_token, sendEmail


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

    token = create_access_token({"email": new_user.email})

    sendEmail(new_user.email, token)

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


@router.post('/verify-email/{token}', status_code=status.HTTP_200_OK)
def verify_email(token, db: Session = Depends(get_db)):
    payload = verify_access_token(token)

    new_user = db.query(models.User).filter(models.User.email==payload['email'])

    if not new_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    new_user.update({"is_active":True})
    db.commit()
    return {}


@router.post('/password/reset', status_code=status.HTTP_200_OK)
def reset_password(request: schemas.UserBase, db:Session = Depends(get_db)):
    email = request.email
    
    user = db.query(models.User).filter(models.User.email==request.email).first()
    
    try:
        token = create_access_token({"email": user.email, "id":user.id}, timedelta(hours=1))
        sendEmail(user.email, token)

    except:
        pass

    return {"data": "Email will be sent, if specified email is valid"}

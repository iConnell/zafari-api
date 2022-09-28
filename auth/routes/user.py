from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..utils import get_current_user, get_db


router = APIRouter(
    prefix='/api/profile',
    tags=['User Profile']
    )

@router.put('', status_code=status.HTTP_201_CREATED, response_model=schemas.ReadUser)
def create_profile(request: schemas.CreateProfile, user: schemas.ReadUser = Depends(get_current_user), db:Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id==user.id).update(request.dict())
    db.commit()
    db.refresh(user)
    return user


@router.get('', status_code=status.HTTP_200_OK, response_model=schemas.ReadUser)
def get_profile(user: schemas.ReadUser = Depends(get_current_user)):
    return user
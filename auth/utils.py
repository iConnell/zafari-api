from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt
from .models import User
from .database import get_db
from sqlalchemy.orm import Session

# for development purposes only
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer('login')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_user(id:int, db: Session):
    
    user = db.query(User).filter(User.id==id).first()
    return user

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_in: timedelta | None = None):
    data_to_encode = data.copy()

    if expires_in:
        expire = datetime.utcnow() + expires_in
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        user = get_user(id, db)
        return user
        
    except Exception as e:
        print(e)
        raise credentials_exception


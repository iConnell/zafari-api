from pydantic import BaseModel

class ChangePasswordSchema(BaseModel):
    password1:str
    password2:str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class CreateProfile(UserBase):
    email: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    phone: str | None = None

class ReadUser(UserBase):
    id: int
    username: str | None = None
    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    is_active: bool
    gender: str | None = None
    
    class Config:
        orm_mode = True

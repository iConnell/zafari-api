from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class ReadUser(UserBase):
    id: int
    username: str | None = None
    email: str
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool
    
    class Config:
        orm_mode = True

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class ReadUser(UserBase):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    
    class Config:
        orm_mode = True

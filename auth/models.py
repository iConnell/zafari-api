from datetime import datetime
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.types import DateTime
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    # gender = Column
    is_active = Column(Boolean, default=False)
    date_joined = Column(DateTime(timezone=True), default=datetime.utcnow())
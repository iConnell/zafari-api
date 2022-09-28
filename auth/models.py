from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.types import DateTime
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, nullable=True, unique=True)
    password = Column(String)
    first_name = Column(String, nullable=True,)
    last_name = Column(String, nullable=True,)
    phone = Column(String, nullable=True)
    gender = Column(String)
    is_active = Column(Boolean, default=False, nullable=True,)
    date_joined = Column(DateTime(timezone=True), default=datetime.utcnow())

    @validates('gender')
    def validate_gender(self, key, value):
        if value != 'm' or value != 'f':
            raise ValueError("Valid values for gender is 'm' and 'f'")
        return value
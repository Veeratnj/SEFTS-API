from app.db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float,Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50),nullable=False)
    age=Column(Integer,)
    gender = Column(String(10))
    is_subscribe = Column(Boolean, nullable=False,default=False)


    
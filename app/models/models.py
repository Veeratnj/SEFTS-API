from app.db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float,Boolean
from sqlalchemy.orm import relationship


# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), nullable=False)
#     email = Column(String(50),nullable=False)
#     age=Column(Integer,)
#     gender = Column(String(10))
#     is_subscribe = Column(Boolean, nullable=False,default=False)


class StockDetails(Base):
    __tablename__ = 'stock_details'
    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    ltp = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False)
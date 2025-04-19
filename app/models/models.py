from app.db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))

    active_strategies = relationship("UserActiveStrategy", back_populates="user")


class StockDetails(Base):
    __tablename__ = 'stock_details'
    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    ltp = Column(Integer, nullable=False)
    last_update = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Corrected: This establishes the reverse relationship with UserActiveStrategy
    active_strategies = relationship("UserActiveStrategy", back_populates="stock_details")


class Strategy(Base):
    __tablename__ = 'strategy'
    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String, nullable=False)
    uuid = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=False, default=0)
    is_deleted = Column(Boolean, nullable=False, default=False)
    deleted_at = Column(DateTime, nullable=True, default=None)
    deleted_by = Column(Integer, nullable=True, default=None)

    active_strategies = relationship("UserActiveStrategy", back_populates="strategy")


class UserActiveStrategy(Base):
    __tablename__ = 'user_active_strategy'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    strategy_id = Column(String, ForeignKey('strategy.uuid'))
    stock_token = Column(String, ForeignKey('stock_details.token'), nullable=False)

    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    deactivated_at = Column(DateTime, nullable=True, default=None)
    deactivated_by = Column(Integer, nullable=True, default=None)

    # Relationships
    user = relationship("User", back_populates="active_strategies")
    strategy = relationship("Strategy", back_populates="active_strategies")
    stock_details = relationship("StockDetails", back_populates="active_strategies")

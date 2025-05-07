from app.db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    mobile = Column(String(15), nullable=False)
    password = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    role = Column(String(20), nullable=False)
    active_strategies = relationship("UserActiveStrategy", back_populates="user")
    login_track = relationship("LoginTrack", back_populates="user")

class LoginTrack(Base):
    __tablename__ = 'login_track'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    token = Column(String, unique=True, nullable=False)
    login_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    logout_time = Column(DateTime, nullable=True)
    ip_address = Column(String(50), nullable=False)
    device_info = Column(String(100), nullable=False)
    user = relationship("User", back_populates="login_track")


# class UserBrokerAccount(Base):
#     __tablename__ = 'user_broker_account'
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     broker_name = Column(String(50), nullable=False)
#     account_number = Column(String(50), unique=True, nullable=False)
#     api_key = Column(String(100), unique=True, nullable=False)
#     secret_key = Column(String(100), unique=True, nullable=False)
#     totp=Column(String, nullable=False)
#     pin=Column(Integer, nullable=False)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
#     updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

#     user = relationship("User", back_populates="user_broker_account")


class Stocks(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    exchange = Column(String, nullable=False)
    is_hotlist = Column(Boolean, nullable=False, default=False)
    trend_type = Column(String, nullable=False)  # 'bullish' or 'bearish'
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=False, default=0)
    is_deleted = Column(Boolean, nullable=False, default=False)


class StockDetails(Base):
    __tablename__ = 'stock_details'
    id = Column(Integer, primary_key=True, index=True)
    stock_name = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    ltp = Column(Float, nullable=False)
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
    trade_count = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    paper_trade = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)
    is_started = Column(Boolean, nullable=False, default=False)
    deactivated_at = Column(DateTime, nullable=True, default=None)
    deactivated_by = Column(Integer, nullable=True, default=None)
    status = Column(String, nullable=False, default='pending')  # 'pending' 'active', 'close', 'rejected'

    # Relationships
    user = relationship("User", back_populates="active_strategies")
    strategy = relationship("Strategy", back_populates="active_strategies")
    stock_details = relationship("StockDetails", back_populates="active_strategies")
    order_managers = relationship("OrderManager", back_populates="user_active_strategy")


class OrderManager(Base):
    __tablename__ = 'order_manager'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, nullable=False)
    completed_order_count = Column(Integer, nullable=False, default=0)
    buy_count = Column(Integer, nullable=False, default=0)
    sell_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # New foreign key
    user_active_strategy_id = Column(Integer, ForeignKey('user_active_strategy.id'), nullable=False)

    # Relationships
    user_active_strategy = relationship("UserActiveStrategy", back_populates="order_managers")


class EquityTradeHistory(Base):
    __tablename__ = 'equity_trade_history'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey('order_manager.order_id'))
    stock_token = Column(String, ForeignKey('stock_details.token'))
    trade_type = Column(String, nullable=False)  # 'buy' or 'sell'
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    entry_ltp=Column(Float, nullable=False)
    exit_ltp=Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    trade_entry_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    trade_exit_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    order_manager = relationship("OrderManager")
    stock_details = relationship("StockDetails")




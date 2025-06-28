from pydantic import BaseModel, EmailStr
from typing import Any, List, Optional, Union
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[str] = None
    is_subscribe: bool
    class Config:
        orm_mode = True




class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    is_subscribe: Optional[bool] = None


class CommonResponse(BaseModel):
    status:int
    data: Union[List[Any], Any]
    msg:str


class AddStrategyRequest(BaseModel):
    strategy_name: str
    strategy_uuid: str
    stock_name: str
    stock_token: str
    quantity:int
    trade_count:int
    user_id:int



class TradeHistoryResponse(BaseModel):
    id: int
    stock_name: str
    order_id: str
    stock_token: str
    trade_type: str
    quantity: int
    price: float
    entry_ltp: float
    exit_ltp: float
    total_price: float
    trade_entry_time: datetime
    trade_exit_time: datetime
    pnl: float

    class Config:
        from_attributes = True


class StocksSchema(BaseModel):
    stock_name: str
    token: str
    exchange: str
    is_hotlist: bool
    trend_type: str
    created_at: datetime
    updated_at: datetime
    created_by: int
    is_deleted: bool

    class Config:
        from_attributes = True


class StockDetailsSchema(BaseModel):
    stock_name: str
    token: str
    ltp: float
    last_update: datetime

    class Config:
        from_attributes = True

class TradeHistoryRequest(BaseModel):
    user_id: int
    flag: int
    limit: int = 100
    offset: int = 0
    type: str | None = None  # Optional field
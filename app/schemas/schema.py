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

    class Config:
        orm_mode = True
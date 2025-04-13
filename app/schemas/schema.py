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

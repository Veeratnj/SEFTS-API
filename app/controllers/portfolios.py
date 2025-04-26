from app.schemas.schema import CommonResponse
from fastapi import APIRouter, HTTPException ,Depends
from pydantic import BaseModel
from app.services.login_services import authenticate_user
from app.cryptography.crypt import decrypt
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.dashboard_services import (
    get_orders_services,
)



router = APIRouter()

@router.get("/get/pending/orders")
def get_all_pending_orders( user_id: int,db: Session = Depends(get_db)):
    try:
        result=get_orders_services(user_id=user_id,db=db,order_type='pending')
        return CommonResponse(
            status=200,
            data=result,
            msg="pending orders fetched successfully"
        )
    except Exception as e:  
        print("Error during fetching pending orders:", str(e))
        return CommonResponse(
            status=500,
            data={},
            msg="Failed to fetch pending orders"
        )


@router.get("/get/active/orders")
def get_all_active_orders( user_id: int,db: Session = Depends(get_db)):

    try:
        result=get_orders_services(user_id=user_id,db=db,order_type='active')
        return CommonResponse(
            status=200,
            data=result,
            msg="Active orders fetched successfully"
        )
    except Exception as e:  
        print("Error during fetching active orders:", str(e))
        return CommonResponse(
            status=500,
            data={},
            msg="Failed to fetch active orders"
        )
    
    
@router.get("/get/close/orders")
def get_all_closed_orders( user_id: int,db: Session = Depends(get_db)):
    try:
        result=get_orders_services(user_id=user_id,db=db,order_type='close')
        return CommonResponse(
            status=200,
            data=result,
            msg="close orders fetched successfully"
        )
    except Exception as e:  
        print("Error during fetching close orders:", str(e))
        return CommonResponse(
            status=500,
            data={},
            msg="Failed to fetch close orders"
        )

@router.get("/get/rejected/orders")
def get_all_open_orders(user_id: int,db: Session = Depends(get_db)):
    try:
        result=get_orders_services(user_id=user_id,db=db,order_type='rejected')
        return CommonResponse(
            status=200,
            data=result,
            msg="rejected orders fetched successfully"
        )
    except Exception as e:  
        print("Error during fetching active orders:", str(e))
        return CommonResponse(
            status=500,
            data={},
            msg="Failed to fetch rejected orders"
        )


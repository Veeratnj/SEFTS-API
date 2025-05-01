from typing import List
from app.models.models import EquityTradeHistory, OrderManager, StockDetails, UserActiveStrategy
from app.schemas.schema import CommonResponse, TradeHistoryResponse
from fastapi import APIRouter, HTTPException ,Depends
from pydantic import BaseModel
from app.services.login_services import authenticate_user
from app.cryptography.crypt import decrypt
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.services.dashboard_services import (
    get_barchart_data_services,
    get_orders_services,
    get_piechart_data_services,
    get_speedometer_data_service,
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


@router.get("/trade-history/{user_id}", response_model=List[TradeHistoryResponse])
def get_trade_history(user_id: int, db: Session = Depends(get_db)):
    # Get all UserActiveStrategy IDs for the user
    user_strategies = db.query(UserActiveStrategy).filter(UserActiveStrategy.user_id == user_id).all()

    if not user_strategies:
        raise HTTPException(status_code=404, detail="User not found or has no active strategies")

    strategy_ids = [strategy.id for strategy in user_strategies]

    # Get all OrderManagers related to these strategies
    orders = db.query(OrderManager).filter(OrderManager.user_active_strategy_id.in_(strategy_ids)).all()
    order_ids = [order.order_id for order in orders]

    # Join EquityTradeHistory with StockDetails to fetch stock_name
    trades = (
        db.query(
            EquityTradeHistory,
            StockDetails.stock_name
        )
        .join(StockDetails, EquityTradeHistory.stock_token == StockDetails.token)
        .filter(EquityTradeHistory.order_id.in_(order_ids))
        .all()
    )

    # Format the response using the schema
    trade_responses = [
    TradeHistoryResponse(
        id=trade.id,
        stock_name=stock_name,
        order_id=trade.order_id,
        stock_token=trade.stock_token,
        trade_type=trade.trade_type,
        quantity=trade.quantity,
        price=trade.price,
        entry_ltp=trade.entry_ltp,
        exit_ltp=trade.exit_ltp,
        total_price=trade.total_price,
        trade_entry_time=trade.trade_entry_time,
        trade_exit_time=trade.trade_exit_time,
        pnl=round(
            trade.price - trade.total_price if trade.trade_type == 'sell'
            else trade.total_price - trade.price,
            2
        ),
    )
    for trade, stock_name in trades
]

    return trade_responses




@router.get("/get/piechart/data")
def get_piechart_data(user_id: int,db: Session = Depends(get_db)):
    
    
    try:
        result=get_piechart_data_services(user_id=user_id,db=db,)
        return CommonResponse(
                status=200,
                data=result,
                msg="piechart data fetched successfully"
            )
    except Exception as e:  
        print("Error during fetching active orders:", str(e))
        return CommonResponse(
            status=500,
            data={'error': str(e)},
            msg="Failed to fetch piechart data"
        )



@router.get("/get/barchart/details")
def get_bar_chart_data(user_id: int,filter:str,db: Session = Depends(get_db)):
    try:
        result=get_barchart_data_services(user_id=user_id,db=db,filter=filter)
        return CommonResponse(
                status=200,
                data=result,
                msg="bar chart data fetched successfully"
            )
    except Exception as e:  
        print("Error during fetching active orders:", str(e))
        return CommonResponse(
            status=500,
            data={'error': str(e)},
            msg="Failed to fetch bar chart data"
        )


@router.get("/get/speedometer/details")
def get_speedometer_data(user_id: int,db: Session = Depends(get_db)):
    try:
        result=get_speedometer_data_service(user_id=user_id,db=db,)
        return CommonResponse(
                status=200,
                data=result,
                msg="speedometer data fetched successfully"
            )
    except Exception as e:  
        print("Error during fetching active orders:", str(e))
        return CommonResponse(
            status=500,
            data={'error': str(e)},
            msg="Failed to fetch speedometer data"
        )
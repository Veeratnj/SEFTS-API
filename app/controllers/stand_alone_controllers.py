from datetime import datetime
from fastapi import Depends
from requests import Session
from app.db.db import get_db
from app.models.models import EquityTradeHistory, OHLCData, OrderManager, StockDetails
from app.schemas.schema import CommonResponse, OrderManagerCreateRequest, TradeEntryRequest, TradeExitRequest
from fastapi import APIRouter, HTTPException ,Depends, Query
from sqlalchemy import update


router = APIRouter()

@router.get('/get/ltp', response_model=CommonResponse)
def get_latest_ltp(stock_token: str, db: Session = Depends(get_db)):
    result = (
        db.query(StockDetails.last_update, StockDetails.ltp, StockDetails.symbol)
        .filter(StockDetails.token == stock_token)
        .order_by(StockDetails.last_update.desc())
        .limit(1)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail=f"No LTP found for token {stock_token}")

    return CommonResponse(
        status=1,
        msg="LTP fetched successfully",
        data={
            "token": stock_token,
            "ltp": result[1],
            "last_update": result[0],
            "symbol": result[2]
        }
    )


@router.get('/get/ohlc', response_model=CommonResponse)
def get_latest_ohlc(stock_token: str, db: Session = Depends(get_db)):
    latest_ohlc = (
        db.query(OHLCData)
        .filter(OHLCData.token == stock_token)
        .order_by(OHLCData.id.desc(), OHLCData.start_time.desc())
        .limit(1)
        .first()
    )

    if not latest_ohlc:
        raise HTTPException(status_code=404, detail=f"No OHLC data found for token {token}")

    return CommonResponse(
    status=1,
    msg="OHLC data fetched successfully",   
    data={
        "id": latest_ohlc.id,
        "token": latest_ohlc.token,
        "start_time": latest_ohlc.start_time,
        "open": float(latest_ohlc.open),
        "high": float(latest_ohlc.high),
        "low": float(latest_ohlc.low),
        "close": float(latest_ohlc.close),
        "interval": latest_ohlc.interval,
        "created_at": latest_ohlc.created_at
    }
)


@router.post('/order/manager/create', response_model=CommonResponse)
def create_order_manager(request: OrderManagerCreateRequest, db: Session = Depends(get_db)):
    # Check if order_id already exists
    existing_order = db.query(OrderManager).filter(OrderManager.order_id == request.order_id).first()

    if existing_order:
        return CommonResponse(
            status=1,
            msg="Order already exists, no insertion performed",
            data={"order_id": request.order_id}
        )

    # Create new OrderManager using ORM
    new_order = OrderManager(
        order_id=request.order_id,
        completed_order_count=request.completed_order_count,
        buy_count=request.buy_count,
        sell_count=request.sell_count,
        is_active=request.is_active,
        created_at=request.created_at,
        updated_at=request.updated_at,
        user_active_strategy_id=request.user_active_strategy_id
    )

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

    return CommonResponse(
        status=1,
        msg="Order Manager created successfully",
        data={
            "order_id": new_order.order_id,
            "user_active_strategy_id": new_order.user_active_strategy_id
        }
    )

@router.post("/trade/entry", response_model=CommonResponse)
def create_trade_entry(payload: TradeEntryRequest, db: Session = Depends(get_db)):

    trade = EquityTradeHistory(
        order_id=payload.order_id,
        stock_token=payload.stock_token,
        trade_type=payload.trade_type,
        quantity=payload.quantity,
        price=payload.price,
        entry_ltp=payload.entry_ltp,
        exit_ltp=payload.exit_ltp,
        total_price=payload.total_price,
        trade_entry_time=payload.trade_entry_time,
        trade_exit_time=payload.trade_exit_time
    )

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return CommonResponse(
        status=True,
        msg="Trade entry created successfully",
        data={"trade_id": trade.id}
    )


@router.post("/trade/exit", response_model=CommonResponse)
def update_trade_exit(payload: TradeExitRequest, db: Session = Depends(get_db)):

    stmt = (
        update(EquityTradeHistory)
        .where(
            EquityTradeHistory.order_id == payload.order_id,
            EquityTradeHistory.trade_type == payload.trade_type,
            EquityTradeHistory.exit_ltp == 0
        )
        .values(
            exit_ltp=payload.exit_ltp,
            trade_exit_time=payload.trade_exit_time or datetime.utcnow(),
            total_price=payload.total_price
        )
    )

    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        return CommonResponse(
            status=False,
            msg=f"No matching {payload.trade_type} trade found to update for order_id {payload.order_id}.",
            data={}
        )

    return CommonResponse(
        status=True,
        msg=f"Trade exit updated successfully for {payload.trade_type} order.",
        data={"updated_rows": result.rowcount}
    )




import json
from typing import List
from app.models.models import BankNiftyOptionsTradeHistory, EquityTradeHistory, OrderManager, StockDetails, UserActiveStrategy
from app.schemas.schema import CommonResponse, OptionTradeHistoryRequest, TradeHistoryRequest, TradeHistoryResponse
from fastapi import APIRouter, HTTPException ,Depends, Query
from pydantic import BaseModel
from app.services.login_services import authenticate_user
from app.cryptography.crypt import decrypt
from sqlalchemy.orm import Session
from app.db.db import get_db


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from datetime import datetime, date


router = APIRouter()







@router.get("/trade/open/{user_id}")
def get_open_trades(user_id: int, db: Session = Depends(get_db)):
    today = date.today()  # e.g., 2025-08-03

    trades = (
        db.query(BankNiftyOptionsTradeHistory)
        .filter(
            BankNiftyOptionsTradeHistory.trade_type == "BUY",
            BankNiftyOptionsTradeHistory.exit_price.is_(None),
            BankNiftyOptionsTradeHistory.order_id.like(f"{user_id}_%"),
            BankNiftyOptionsTradeHistory.trade_entry_time >= datetime.combine(today, datetime.min.time()),
            BankNiftyOptionsTradeHistory.trade_entry_time <= datetime.combine(today, datetime.max.time())
        )
        .order_by(BankNiftyOptionsTradeHistory.trade_entry_time.desc())
        .all()
    )
    return trades




@router.get("/trade/closed/{user_id}")
def get_closed_trades(user_id: int, db: Session = Depends(get_db)):
    today = date.today()

    closed_trades = (
        db.query(BankNiftyOptionsTradeHistory)
        .filter(
            BankNiftyOptionsTradeHistory.trade_type == "BUY",
            BankNiftyOptionsTradeHistory.exit_price.isnot(None),
            BankNiftyOptionsTradeHistory.order_id.like(f"{user_id}_%"),
            BankNiftyOptionsTradeHistory.trade_exit_time >= datetime.combine(today, datetime.min.time()),
            BankNiftyOptionsTradeHistory.trade_exit_time <= datetime.combine(today, datetime.max.time())
        )
        .order_by(BankNiftyOptionsTradeHistory.trade_exit_time.desc())
        .all()
    )

    response = []
    total_pnl = 0.0

    for trade in closed_trades:
        pnl = round(trade.exit_price - trade.entry_price, 2)
        total_pnl += pnl

        response.append({
            "order_id": trade.order_id,
            "option_symbol": trade.option_symbol,
            "quantity": trade.quantity,
            "entry_price": trade.entry_price,
            "exit_price": trade.exit_price,
            "pnl": pnl,
            "entry_time": trade.trade_entry_time,
            "exit_time": trade.trade_exit_time
        })
        print(response)

    return {
        "user_id": user_id,
        "date": today.isoformat(),
        "total_pnl": round(total_pnl, 2),
        "closed_trades": response
    }







@router.post("/option/trade-history")
def get_option_trade_history(filters: OptionTradeHistoryRequest, db: Session = Depends(get_db)):
    # Date range based on flag
    today = datetime.now()
    if filters.flag == 1:  # 1D
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif filters.flag == 2:  # 1W
        start_date = today - timedelta(days=7)
    elif filters.flag == 3:  # 1M
        start_date = today - timedelta(days=30)
    elif filters.flag == 4:  # 1Y
        start_date = today - timedelta(days=365)
    else:  # ALL
        start_date = None

    query = db.query(BankNiftyOptionsTradeHistory).filter(
        BankNiftyOptionsTradeHistory.order_id.like(f"{filters.user_id}_%"),
        BankNiftyOptionsTradeHistory.trade_type == "BUY",  # only BUY entries
        BankNiftyOptionsTradeHistory.exit_price.isnot(None)
    )

    if start_date:
        query = query.filter(BankNiftyOptionsTradeHistory.trade_entry_time >= start_date)

    trades = query.order_by(BankNiftyOptionsTradeHistory.trade_entry_time.desc()) \
                  .offset(filters.offset) \
                  .limit(filters.limit) \
                  .all()

    results = []
    for t in trades:
        results.append({
            "option_symbol": t.option_symbol,
            "option_type": t.option_type,
            "entry_ltp": t.entry_ltp,
            "exit_ltp": t.exit_ltp,
            "entry_price": t.entry_price,
            "exit_price": t.exit_price,
            "pnl": round((t.exit_price or 0) - t.entry_price, 2),
            "quantity": t.quantity,
            "trade_entry_time": t.trade_entry_time.isoformat(),
            "trade_exit_time": t.trade_exit_time.isoformat() if t.trade_exit_time else None
        })

    return {
        "data": {
            "records": results,
            "total": len(results)
        }
    }



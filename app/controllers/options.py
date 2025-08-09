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

from app.services.options_service import options_history


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
            "entry_ltp": trade.entry_ltp,
            "exit_ltp": trade.exit_ltp,
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
    try:
        # r=options_history(filters=filters,db=db)
        # print(r)
        return options_history(filters=filters,db=db)
    except Exception as e:
        print(e)
    


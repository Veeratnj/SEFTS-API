import json
from typing import List
from app.db import db
from app.models.models import BankNiftyOptionsTradeHistory, EquityTradeHistory, OrderManager, StockDetails, UserActiveStrategy
from app.schemas.schema import CommonResponse, OptionTradeHistoryRequest, OptionsLTPRequest, TradeHistoryRequest, TradeHistoryResponse
from fastapi import APIRouter, HTTPException ,Depends, Query
from pydantic import BaseModel
from app.services.login_services import authenticate_user
from app.cryptography.crypt import decrypt
from sqlalchemy.orm import Session
from app.db.db import get_db
from sqlalchemy.orm import aliased


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


from datetime import datetime, date

from app.services.options_service import options_history


router = APIRouter()







@router.get("/trade/open1/{user_id}")
def get_open_trades1(user_id: int, db: Session = Depends(get_db)):
    today = date.today()  # e.g., 2025-08-03

    # trades = (
    #     db.query(BankNiftyOptionsTradeHistory)
    #     .join(StockDetails,BankNiftyOptionsTradeHistory.option_symbol==StockDetails.token)
    #     .filter(
    #         BankNiftyOptionsTradeHistory.trade_type == "BUY",
    #         BankNiftyOptionsTradeHistory.exit_price.is_(None),
    #         BankNiftyOptionsTradeHistory.order_id.like(f"{user_id}_%"),
    #         BankNiftyOptionsTradeHistory.trade_entry_time >= datetime.combine(today, datetime.min.time()),
    #         BankNiftyOptionsTradeHistory.trade_entry_time <= datetime.combine(today, datetime.max.time())
    #     )
    #     .order_by(BankNiftyOptionsTradeHistory.trade_entry_time.desc())
    #     .all()
    # )
    bnoth = aliased(BankNiftyOptionsTradeHistory)
    sd = aliased(StockDetails)

    query = (
        db.query(
            bnoth.option_symbol,
            bnoth.option_type,
            bnoth.quantity,
            bnoth.entry_ltp,
            bnoth.trade_entry_time,
            sd.ltp.label("current_ltp"),
            ((sd.ltp - bnoth.entry_ltp) * bnoth.quantity).label("Profit")
        )
        .outerjoin(sd, sd.token == bnoth.option_symbol)  # LEFT JOIN
        .filter(bnoth.order_id.like("3%"))
    )
    result = query.all()

    print(result)
    return result


@router.get("/trade/open/{user_id}")
def get_open_trades(user_id: int, db: Session = Depends(get_db)):
    today = date.today()

    bnoth = aliased(BankNiftyOptionsTradeHistory)
    sd = aliased(StockDetails)

    query = (
        db.query(
            bnoth.option_symbol,
            bnoth.option_type,
            bnoth.quantity,
            bnoth.entry_ltp,
            bnoth.trade_entry_time,
            bnoth.entry_price,
            sd.ltp.label("current_ltp"),
            ((sd.ltp - bnoth.entry_ltp) * bnoth.quantity).label("Profit")
        )
        .outerjoin(sd, sd.token == bnoth.option_symbol)  # LEFT JOIN
        .filter(
            bnoth.trade_type == "BUY",
            bnoth.exit_price.is_(None),
            bnoth.order_id.like(f"{user_id}_%"),
            bnoth.trade_entry_time >= datetime.combine(today, datetime.min.time()),
            bnoth.trade_entry_time <= datetime.combine(today, datetime.max.time())
        )
        .order_by(bnoth.trade_entry_time.desc())
    )

    # Convert to structured dict list
    results = [
        {
            "option_symbol": r.option_symbol,
            "option_type": r.option_type,
            "quantity": r.quantity,
            "entry_ltp": r.entry_ltp,
            "entry_price":r.entry_price,
            "trade_entry_time": r.trade_entry_time,
            "current_ltp": r.current_ltp,
            "profit": r.Profit
        }
        for r in query.all()
    ]

    return results




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
    

from datetime import datetime

@router.post("/insert-or-update-ltp")
def insert_or_update_ltp(payload: OptionsLTPRequest, db: Session = Depends(get_db)):
    try:
        existing_record = db.query(StockDetails).filter(StockDetails.token == payload.option_symbol).first()
        
        if existing_record:
            # Update existing record
            existing_record.ltp = payload.ltp
            existing_record.last_update = datetime.utcnow()
            db.commit()
            return {"message": "LTP updated successfully"}
        else:
            # Insert new record
            new_record = StockDetails(
                stock_name=payload.option_symbol,
                token=payload.option_symbol,
                ltp=payload.ltp,
                symbol=payload.option_symbol,
                last_update=datetime.utcnow()
            )
            db.add(new_record)
            db.commit()
            return {"message": "LTP inserted successfully"}
    except Exception as e:
        db.rollback()
        print(f"Error inserting/updating LTP: {e}")
        raise HTTPException(status_code=500, detail=str(e))
  



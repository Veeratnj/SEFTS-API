from sqlalchemy.orm import Session
from app.db.db import SessionLocal
from app.models.models import StockDetails
from typing import List

import logging
logging.basicConfig(level=logging.DEBUG)

async def get_live_stock_prices1(tokens: List[str]) -> dict:
    live_prices = {}
    db: Session = SessionLocal()
    try:
        db.expire_all()
        stocks = db.query(StockDetails).filter(StockDetails.token.in_(tokens)).all()
        
        for stock in stocks:
            db.refresh(stock) 
            logging.debug(f"Fetched stock: {stock.token}, Price: {stock.ltp}")
            live_prices[stock.token] = {
                "stock_name": stock.stock_name,
                "price": stock.ltp,
                "last_update": stock.last_update.isoformat()
            }
    finally:
        db.close()
    return live_prices
    

async def get_live_stock_prices(tokens: List[str]) -> dict:
    """
    Fetch live stock prices for the given tokens from the database.
    """
    live_prices = {}
    db: Session = SessionLocal()
    try:
        db.expire_all()
        stocks = db.query(StockDetails).filter(StockDetails.token.in_(tokens)).all()
        for stock in stocks:
            db.refresh(stock)  # Ensure fresh data
            live_prices[stock.token] = {
                "stock_name": stock.stock_name,
                "price": stock.ltp,
                "last_update": stock.last_update.isoformat()
            }
    finally:
        db.close()
    return live_prices
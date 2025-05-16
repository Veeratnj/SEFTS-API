from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from app.models.models import EquityTradeHistory, OrderManager, StockDetails, User, UserActiveStrategy, Stocks
from app.schemas.schema import StockDetailsSchema,StocksSchema


def update_model_instance(existing_instance, new_data):
    for column in inspect(existing_instance).mapper.column_attrs:
        key = column.key
        new_value = getattr(new_data, key)
        if new_value is not None:
            setattr(existing_instance, key, new_value)


def add_StockDetails_service(db: Session, stockDetailsSchema: StockDetailsSchema) -> StockDetails:
    try:
        existing_stock = db.query(StockDetails).filter(StockDetails.stock_name == stockDetailsSchema.stock_name).first()
        if existing_stock:
            update_model_instance(existing_stock, stockDetailsSchema)
            db.commit()
            db.refresh(existing_stock)
            return existing_stock

        # Create new ORM object from Pydantic schema
        new_stock = StockDetails(
            stock_name=stockDetailsSchema.stock_name,
            token=stockDetailsSchema.token,
            ltp=stockDetailsSchema.ltp,
            last_update=stockDetailsSchema.last_update,
        )

        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)
        return new_stock

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add/update StockDetails: {str(e)}")
        

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add/update StockDetails: {str(e)}")


def add_stock_services(db: Session, stock: Stocks) -> Stocks:
    try:
        stock=Stocks(**stock.dict())
        existing_stock = db.query(Stocks).filter(Stocks.token == stock.token).first()
        if existing_stock:
            update_model_instance(existing_stock, stock)
            db.commit()
            db.refresh(existing_stock)
            return existing_stock

        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add/update Stock: {str(e)}")



def get_stocks_services(db: Session) -> List[StocksSchema]:
    try:
        stocks = db.query(Stocks).filter(Stocks.is_deleted == False).all()
        return [StocksSchema.from_orm(stock) for stock in stocks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stocks: {str(e)}")


def get_stockDetails_services(db: Session) -> List[StockDetailsSchema]:
    try:
        stock_details = db.query(StockDetails).all()
        return [StockDetailsSchema.from_orm(detail) for detail in stock_details]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stock details: {str(e)}")
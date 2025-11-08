from app.services.adminService import add_StockDetails_service,add_stock_services,get_stocks_services,get_stockDetails_services,get_option_kill_status_service
from app.services.common_services import add_strategy_service, get_all_stock_name_service,get_all_strategies_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.schema import  CommonResponse, StockDetailsSchema,StocksSchema
from app.models.models import StockDetails,Stocks

router = APIRouter()

@router.post("/cud/stocks/details", response_model=CommonResponse)
def create_user(stockDetails: StockDetailsSchema, db: Session = Depends(get_db)):
    try:
        # Check if the stock name already exists
        add_StockDetails_service(db=db, stockDetailsSchema=stockDetails)
              
        return CommonResponse(
            status=200,
            data=[],
            msg="stock details  created successfully"
        )
    except Exception as e:
        print(e)
        return CommonResponse(
            status=500,
            data=str(e),
            msg="Something went wrong"
        )

@router.post("/cud/stocks", response_model=CommonResponse)
def add_stock(stock:StocksSchema, db: Session = Depends(get_db)):
    try:
        # Check if the stock name already exists
        add_stock_services(db=db, stock=stock)
        return CommonResponse(
            status=200,
            data=[],
            msg="stock data   created successfully"
        )
    except Exception as e:
        return CommonResponse(
            status=500,
            data=str(e),
            msg="Something went wrong"
        )
    
@router.get("/get/stocks", response_model=CommonResponse)
def get_all_stock( db: Session = Depends(get_db)):
    try:
        # Assuming you have a function to get all stock names
        all_stock = get_stocks_services(db=db)
        return CommonResponse(
            status=200,
            data=all_stock,
            msg="All stock names retrieved successfully"
        )
    except Exception as e:
        print(e)
        return CommonResponse(
            status=500,
            data=str(e),
            msg="Something went wrong"
        )
    
@router.get("/get/stocks/details", response_model=CommonResponse)
def get_all_stock_details( db: Session = Depends(get_db)):
    try:
        # Assuming you have a function to get all stock names
        all_stock = get_stockDetails_services(db=db)
        return CommonResponse(
            status=200,
            data=all_stock,
            msg="All stock names retrieved successfully"
        )
    except Exception as e:
        return CommonResponse(
            status=500,
            data=str(e),
            msg="Something went wrong"
        )
    


@router.get("/get/option/kill/status", response_model=CommonResponse)
def get_option_kill_status(db: Session = Depends(get_db)):
    try:
        # Assuming you have a function to get all stock names
        status = get_option_kill_status_service(db=db)
        return CommonResponse(
            status=200,
            data=status,
            msg="Option kill status retrieved successfully"
        )
    except Exception as e:
        return CommonResponse(
            status=500,
            data=str(e),
            msg="Something went wrong"
        )
    
    
from app.services.common_services import add_strategy_service, get_all_stock_name_service,get_all_strategies_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.schema import UserBase, CommonResponse,AddStrategyRequest

router = APIRouter()

# @router.post("/add/users/", response_model=CommonResponse)
# def create_user(user: UserBase, db: Session = Depends(get_db)):
#     try:
       
#         new_user = user_add(user=user, db=db)
        

#         return CommonResponse(
#             status=201,
#             data=new_user,
#             msg="User created successfully"
#         )
#     except Exception as e:
#         return CommonResponse(
#             status=500,
#             data=str(e),
#             msg="Something went wrong"
#         )

@router.get("/get/stock/tocken", response_model=CommonResponse)
def get_all_stock_name( db: Session = Depends(get_db)):
    try:
        # print(token)
        # Assuming you have a function to get all stock names
        all_stock_names = get_all_stock_name_service(db=db)
        return CommonResponse(
            status=200,
            data=all_stock_names,
            msg="All stock names retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/strategies")
def get_all_strategies(db: Session = Depends(get_db)):
    try:
        # Assuming you have a function to get all strategies
        all_strategies = get_all_strategies_service(db=db)  # Replace with actual function
        # all_strategies=[{
        #     "strategy_name": "3 EMA",
        #     "uuid": "123qwe",
        # }]
        print(all_strategies)
        return CommonResponse(
            status=200,
            data=all_strategies,
            msg="All strategies retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/post/add/strategy")
def add_strategy(strategy_request: AddStrategyRequest, db: Session = Depends(get_db)):
    try:
        print(strategy_request)
        result = add_strategy_service(db=db, strategy_request=strategy_request) 
    
        return CommonResponse(
            status=201,
            data=result,
            msg="Strategy added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

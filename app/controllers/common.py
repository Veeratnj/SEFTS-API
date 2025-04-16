from app.services.common_services import get_all_stock_name_service
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.schemas.schema import UserBase, CommonResponse

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
        # Assuming you have a function to get all stock names
        all_stock_names = get_all_stock_name_service(db=db)
        return CommonResponse(
            status=200,
            data=all_stock_names,
            msg="All stock names retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

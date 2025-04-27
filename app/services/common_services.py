

from app.models.models import StockDetails,Strategy, UserActiveStrategy


# def user_add(db,user,):
    
#     # db_user = db.query(User).filter(User.email == user.email).first()
#     # if db_user:
#     #     raise HTTPException(status_code=400, detail="Email already registered")
    
#     # Create and save the new user
#     new_user = User(
#         name=user.name,
#         email=user.email,
#         age=user.age,
#         gender=user.gender,
#         is_subscribe=user.is_subscribe
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     result={
#         'name':new_user.name,
#         'age':new_user.age,
#         'email':new_user.email,
#         'gender':new_user.gender,
#         'is_subscribe':new_user.is_subscribe
#     }
#     return result



def get_all_stock_name_service(db):
    try:
    
        result=db.query(StockDetails.stock_name,StockDetails.token,StockDetails.ltp).all()
        print(result)
        output_structured = []

        for stock_name, token, ltp in result:
            output_structured.append({
                "name": stock_name,
                "token": token,
                "points": ltp,
            })

        return output_structured
    except Exception as e:
        print(f"Error retrieving stock names: {e}")
        raise



def get_all_strategies_service(db):
    try:
        result = db.query(Strategy.uuid,Strategy.strategy_name).all()
        print(result)
        # output_structured = []

        
        print(result)
        return  [{'uuid': uuid, 'strategy_name': name} for uuid, name in result]

    except Exception as e:
        print(f"Error retrieving stock names: {e}")
        raise e

def add_strategy_service(db, strategy_request):
    try:
        # Insert into UserActiveStrategy only
        user_active_strategy = UserActiveStrategy(
            user_id=strategy_request.user_id,  # default user
            strategy_id=strategy_request.strategy_uuid,  # FK to Strategy.uuid
            stock_token=strategy_request.stock_token,    # FK to StockDetails.token
            quantity=strategy_request.quantity,           # user-defined quantity
            trade_count=strategy_request.trade_count,    # user-defined trade count
            is_started=False,  # default value
        )
        db.add(user_active_strategy)
        db.commit()

        return 'Strategy added successfully to your watchlist.'

    except Exception as e:
        db.rollback()
        print(f"Error adding strategy to user watchlist: {e}")
        raise e
    
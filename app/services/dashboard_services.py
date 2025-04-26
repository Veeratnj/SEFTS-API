




from sqlalchemy.orm import joinedload
from app.models.models import EquityTradeHistory, OrderManager, StockDetails, User, UserActiveStrategy


def get_all_active_orders_services( user_id: int,db):
    pass
    

def get_all_closed_orders_services( user_id: int,db):
    pass


def get_all_open_orders_services(user_id: int,db):
    pass


def get_all_pending_orders_services( user_id: int,db):
    pass


def get_orders_services(user_id: int,order_type,db,):

    pass




def get_orders_services(user_id: int, order_type: str, db):
    query = db.query(
        StockDetails.stock_name,
        UserActiveStrategy.quantity,
        EquityTradeHistory.trade_type,
        EquityTradeHistory.entry_ltp
    ).join(
        OrderManager, UserActiveStrategy.id == OrderManager.user_active_strategy_id
    ).join(
        EquityTradeHistory, OrderManager.order_id == EquityTradeHistory.order_id
    ).join(
        StockDetails, UserActiveStrategy.stock_token == StockDetails.token
    ).filter(
        UserActiveStrategy.user_id == user_id
    )


    

    # Apply status-based filtering
    if order_type == "close":
        query = query.filter(UserActiveStrategy.status == 'close')
    elif order_type == "active":
        query = query.filter(UserActiveStrategy.status == 'active')
    elif order_type == "pending":

        query = db.query(
        StockDetails.stock_name,
        UserActiveStrategy.quantity,
        StockDetails.ltp
    ).join(
        User, User.id == UserActiveStrategy.user_id
    ).join(
        StockDetails, UserActiveStrategy.stock_token == StockDetails.token
    ).filter(
        User.id == user_id,
        UserActiveStrategy.status == 'pending'
    )

        # query = query.filter(UserActiveStrategy.status == 'pending' )

    elif order_type == "rejected":
        query = query.filter(UserActiveStrategy.status == 'rejected')
    else:
        return []

    records = query.all()

    result = []
    for idx, record in enumerate(records):
        stock_name = record.stock_name if hasattr(record, 'stock_name') else None
        quantity = record.quantity if hasattr(record, 'quantity') else None
        trade_type = record.trade_type if hasattr(record, 'trade_type') else None
        entry_ltp = record.entry_ltp if hasattr(record, 'entry_ltp') else None
        ltp = record.ltp if hasattr(record, 'ltp') else None

        result.append({
            "key": idx + 1,
            "stockName": stock_name,
            "orderType": trade_type,
            "qty": quantity,
            "atp": entry_ltp,
            "ltp": ltp if ltp else entry_ltp,  # for pending, use ltp
            "gainLoss": None,
            "sl": None,
            "tg": None,
            'rejected_time': None,
        })


    return result







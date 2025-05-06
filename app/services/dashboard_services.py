


from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import case
from sqlalchemy import func
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






def get_orders_services1(user_id: int, order_type: str, db):
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
        UserActiveStrategy.user_id == user_id,
        func.date(EquityTradeHistory.trade_entry_time) == datetime.utcnow().date()
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

def get_orders_services(user_id: int, order_type: str, db):
    query = db.query(
        StockDetails.stock_name,
        UserActiveStrategy.quantity,
        EquityTradeHistory.trade_type,
        EquityTradeHistory.entry_ltp,
        EquityTradeHistory.exit_ltp,
        EquityTradeHistory.total_price,
        EquityTradeHistory.price
    ).join(
        OrderManager, UserActiveStrategy.id == OrderManager.user_active_strategy_id
    ).join(
        EquityTradeHistory, OrderManager.order_id == EquityTradeHistory.order_id
    ).join(
        StockDetails, UserActiveStrategy.stock_token == StockDetails.token
    ).filter(
        UserActiveStrategy.user_id == user_id,
        func.date(EquityTradeHistory.trade_entry_time) == datetime.utcnow().date()
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
        exit_ltp = record.exit_ltp if hasattr(record, 'exit_ltp') else None
        total_price = record.total_price if hasattr(record, 'total_price') else None
        price = record.price if hasattr(record, 'price') else None
        ltp = record.ltp if hasattr(record, 'ltp') else None

        # Calculate gain or loss
        gain_loss = None
        if trade_type == "buy":
            # For buy: total_price - price
            if total_price and price:
                gain_loss = total_price - price
        elif trade_type == "sell":
            # For sell: price - total_price
            if price and total_price:
                gain_loss = price - total_price

        # Round off the gain_loss to 2 decimal places
        if gain_loss is not None:
            gain_loss = round(gain_loss, 2)*quantity

        result.append({
            "key": idx + 1,
            "stockName": stock_name,
            "orderType": trade_type,
            "qty": quantity,
            "atp": entry_ltp,
            "ltp": ltp if ltp else entry_ltp,  # for pending, use ltp
            "gainLoss": gain_loss,
            "sl": None,
            "tg": None,
            'rejected_time': None,
        })

    return result


def get_piechart_data_services1(user_id: int,filter:str, db: Session):
    # Fetch raw data from the database
    now = datetime.utcnow()
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        # Default to all-time if no valid filter is provided
        start_time = None


    raw_data = db.query(
        EquityTradeHistory.total_price,
        EquityTradeHistory.price
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).filter(
        UserActiveStrategy.user_id == user_id
    ).all()

    # query = query.filter(EquityTradeHistory.trade_entry_time >= start_time)


    # Initialize variables for calculations
    total_profit = 0
    total_investment = 0

    # Perform calculations in Python
    for record in raw_data:
        total_profit += record.total_price - record.price
        total_investment += record.price

    # Avoid division by zero
    if total_investment > 0:
        profit_percentage = round((total_profit * 100.0) / total_investment, 2)
        investment_percentage = round(100.0 - profit_percentage, 2)
    else:
        profit_percentage = 0
        investment_percentage = 0

    # Return the calculated data
    return {
        'profit': round(total_profit, 2),
        'total_investment': round(total_investment, 2),
        'profit_percentage': profit_percentage,
        'investment_percentage': investment_percentage
    }


def get_piechart_data_services2(user_id: int, filter: str, db: Session):
    # Fetch raw data from the database
    now = datetime.utcnow()
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        # Default to all-time if no valid filter is provided
        start_time = None

    # Build the query
    raw_data_query = db.query(
        EquityTradeHistory.total_price,
        EquityTradeHistory.price
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).filter(
        UserActiveStrategy.user_id == user_id
    )

    # Apply the time filter if a valid start_time is determined
    if start_time:
        raw_data_query = raw_data_query.filter(EquityTradeHistory.trade_entry_time >= start_time)

    # Execute the query and fetch results
    raw_data = raw_data_query.all()

    # Initialize variables for calculations
    total_profit = 0
    total_investment = 0
    print(raw_data)
    # Perform calculations in Python
    for record in raw_data:
        total_profit += record.total_price - record.price
        total_investment += record.price

    # Avoid division by zero
    if total_investment > 0:
        profit_percentage = round((total_profit * 100.0) / total_investment, 2)
        investment_percentage = round(100.0 - profit_percentage, 2)
    else:
        profit_percentage = 0
        investment_percentage = 0

    # Return the calculated data
    return {
        'profit': round(total_profit, 2),
        'total_investment': round(total_investment, 2),
        'profit_percentage': profit_percentage,
        'investment_percentage': investment_percentage
    }

def get_piechart_data_services(user_id: int, filter: str, db: Session):
    now = datetime.utcnow()

    # Determine filter range
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        start_time = None

    # Build query
    raw_data_query = db.query(
        EquityTradeHistory.total_price,
        EquityTradeHistory.price,
        EquityTradeHistory.trade_type  # Assuming 'trade_type' exists, with values 'buy' or 'sell'
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).filter(
        UserActiveStrategy.user_id == user_id
    )

    if start_time:
        raw_data_query = raw_data_query.filter(EquityTradeHistory.trade_entry_time >= start_time)

    raw_data = raw_data_query.all()

    total_profit = 0
    total_loss = 0
    total_investment = 0

    for record in raw_data:
        # Calculate profit/loss based on trade type (buy or sell)
        if record.trade_type == "buy":
            diff = record.total_price - record.price
        elif record.trade_type == "sell":
            diff = record.price - record.total_price
        else:
            continue  # If there's any invalid trade type, skip it.

        if diff > 0:
            total_profit += diff
        elif diff < 0:
            total_loss += abs(diff)

        total_investment += record.price

    # Calculate percentages
    total_profit_and_loss = total_profit + total_loss
    if total_profit_and_loss > 0:
        profit_percentage = round((total_profit * 100.0) / total_profit_and_loss, 2)
        loss_percentage = round((total_loss * 100.0) / total_profit_and_loss, 2)
    else:
        profit_percentage = 0
        loss_percentage = 0

    # Calculate profit per lakh
    if total_investment > 0:
        profit_per_lakh = round((total_profit / total_investment) * 100000, 2)
    else:
        profit_per_lakh = 0

    total_returns = total_profit - total_loss

    return {
        'profit': round(total_profit, 2),
        'loss': round(total_loss, 2),
        'total_investment': round(total_investment, 2),
        'profit_percentage': profit_percentage,
        'loss_percentage': loss_percentage,
        'profit_per_lakh': profit_per_lakh,
        'total_returns': round(total_returns + total_investment, 2)
    }


def get_barchart_data_services(user_id: int, filter: str, db: Session):
    # Determine the time range based on the filter
    now = datetime.utcnow()
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        # Default to all-time if no valid filter is provided
        start_time = None

    # Build the query
    query = db.query(
        StockDetails.stock_name,
        func.sum(EquityTradeHistory.price).label('total_investment'),
        func.sum(
            case(
                (EquityTradeHistory.trade_type == 'buy', EquityTradeHistory.total_price - EquityTradeHistory.price),
                (EquityTradeHistory.trade_type == 'sell', EquityTradeHistory.price - EquityTradeHistory.total_price),
                else_=0
            )
        ).label('total_profit_or_loss')
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).join(
        StockDetails, UserActiveStrategy.stock_token == StockDetails.token
    ).filter(
        UserActiveStrategy.user_id == user_id
    )

    # Apply the time filter if a valid start_time is determined
    if start_time:
        query = query.filter(EquityTradeHistory.trade_entry_time >= start_time)

    # Group by stock name
    query = query.group_by(StockDetails.stock_name)

    # Execute the query and fetch results
    raw_data = query.all()

    # Prepare the result
    result = []
    for record in raw_data:
        result.append({
            "stockName": record.stock_name,
            "totalInvestment": round(record.total_investment, 2),
            "totalProfitOrLoss": round(record.total_profit_or_loss, 2)
        })

    return result



def get_speedometer_data_service1(user_id: int,filter:str, db: Session):
    now = datetime.utcnow()
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        # Default to all-time if no valid filter is provided
        start_time = None

    # Fetch total investment and total returns
    data = db.query(
        func.sum(EquityTradeHistory.price).label('total_investment'),
        func.sum(EquityTradeHistory.total_price).label('total_returns')
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).filter(
        UserActiveStrategy.user_id == user_id
    ).first()

    # Prepare the result
    return {
        "overallInvestment": round(data.total_investment, 2) if data.total_investment else 0,
        "overallReturns": round(data.total_returns, 2) if data.total_returns else 0
    }


def get_speedometer_data_service2(user_id: int, filter: str, db: Session):
    now = datetime.utcnow()

    # Determine the start_time based on the filter
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        # Default to all-time if no valid filter is provided
        start_time = None

    # Build the query based on the filter
    query = db.query(
        EquityTradeHistory.price,
        EquityTradeHistory.total_price
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).filter(
        UserActiveStrategy.user_id == user_id
    )

    # Apply the time filter if a valid start_time is determined
    if start_time:
        query = query.filter(EquityTradeHistory.trade_entry_time >= start_time)

    # Execute the query to get the relevant data
    data = query.all()

    # Calculate total investment and total returns
    total_investment = sum(record.price for record in data)
    total_returns = sum(record.total_price for record in data)

    # Return the result
    return {
        "overallInvestment": round(total_investment, 2) if total_investment else 0,
        "overallReturns": round(total_returns, 2) if total_returns else 0
    }

# from datetime import datetime, timedelta
# from sqlalchemy import case, func


def get_speedometer_data_service(user_id: int, filter: str, db: Session):
    now = datetime.utcnow()

    # Determine the start_time based on the filter
    if filter == "1d":
        start_time = now - timedelta(days=1)
    elif filter == "1w":
        start_time = now - timedelta(weeks=1)
    elif filter == "1m":
        start_time = now - timedelta(days=30)
    elif filter == "6m":  # Example: 6 months filter
        start_time = now - timedelta(days=180)
    elif filter == "1y":
        start_time = now - timedelta(days=365)
    else:
        # Default to all-time if no valid filter is provided
        start_time = None

    # Build the query
    query = db.query(
        func.sum(
            case(
                (EquityTradeHistory.trade_type == 'buy', 
                 func.greatest(EquityTradeHistory.total_price - EquityTradeHistory.price, 0)),
                (EquityTradeHistory.trade_type == 'sell', 
                 func.greatest(EquityTradeHistory.price - EquityTradeHistory.total_price, 0)),
                else_=0
            )
        ).label('total_profit'),
        func.sum(
            case(
                (EquityTradeHistory.trade_type == 'buy', 
                 func.greatest(EquityTradeHistory.price - EquityTradeHistory.total_price, 0)),
                (EquityTradeHistory.trade_type == 'sell', 
                 func.greatest(EquityTradeHistory.total_price - EquityTradeHistory.price, 0)),
                else_=0
            )
        ).label('total_loss')
    ).join(
        OrderManager, EquityTradeHistory.order_id == OrderManager.order_id
    ).join(
        UserActiveStrategy, OrderManager.user_active_strategy_id == UserActiveStrategy.id
    ).join(
        StockDetails, StockDetails.token == EquityTradeHistory.stock_token
    ).filter(
        UserActiveStrategy.user_id == user_id
    )

    # Apply the time filter if a valid start_time is determined
    if start_time:
        query = query.filter(EquityTradeHistory.trade_entry_time >= start_time)

    # Execute the query
    result = query.first()

    # Return the result as a dictionary
    return {
    "total_profit": round(result.total_profit, 2) if result.total_profit else 0,
    "total_loss": round(result.total_loss, 2) if result.total_loss else 0
    }
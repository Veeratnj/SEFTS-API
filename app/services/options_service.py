















from datetime import datetime, timedelta

from app.models.models import BankNiftyOptionsTradeHistory



def options_history(filters, db):
    today = datetime.now()
    from_date = filters.from_date
    to_date = filters.to_date

    # Auto-fill date range if not provided
    if not from_date or not to_date:
        if filters.flag == 1:  # 1D
            from_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            to_date = today
        elif filters.flag == 2:  # 1W
            from_date = today - timedelta(days=7)
            to_date = today
        elif filters.flag == 3:  # 1M
            from_date = today - timedelta(days=30)
            to_date = today
        elif filters.flag == 4:  # 1Y
            from_date = today - timedelta(days=365)
            to_date = today
        elif filters.flag == 5:  # ALL
            from_date = None
            to_date = None

    # Base query
    query = db.query(BankNiftyOptionsTradeHistory).filter(
        BankNiftyOptionsTradeHistory.order_id.like(f"{filters.user_id}_%"),
        BankNiftyOptionsTradeHistory.trade_type == "BUY",
        BankNiftyOptionsTradeHistory.exit_price.isnot(None)
    )

    # Apply date filter if needed
    if from_date and to_date:
        query = query.filter(
            BankNiftyOptionsTradeHistory.trade_entry_time >= from_date,
            BankNiftyOptionsTradeHistory.trade_entry_time <= to_date
        )

    # Pagination + sorting
    trades = (
        query.order_by(BankNiftyOptionsTradeHistory.trade_entry_time.desc())
        .offset(filters.offset)
        .limit(filters.limit)
        .all()
    )

    # Prepare results
    results = [
        {
            "option_symbol": t.option_symbol,
            "option_type": t.option_type,
            "entry_ltp": t.entry_ltp,
            "exit_ltp": t.exit_ltp,
            "entry_price": t.entry_price,
            "exit_price": t.exit_price,
            "pnl": round((t.exit_price or 0) - t.entry_price, 2),
            "quantity": t.quantity,
            "trade_entry_time": t.trade_entry_time.isoformat(),
            "trade_exit_time": t.trade_exit_time.isoformat() if t.trade_exit_time else None
        }
        for t in trades
    ]

    return {
        "data": {
            "records": results,
            "total": len(results)
        }
    }







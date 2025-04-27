from app.models.models import User, LoginTrack, Stocks, StockDetails, Strategy, UserActiveStrategy, OrderManager, EquityTradeHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.db import Base
from datetime import datetime

# Database URL (you can modify this as per your actual database)
DATABASE_URL = "postgresql://setc:admin%40123@localhost/setc"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Step 1: Insert data into the user table (Parent)
user_1 = User(
    name="raja",
    email="raja@test.com",
    mobile="8248831127",
    password="admin@123",
    age=27,
    gender="M",
    role="user"
)
session.add(user_1)
session.commit()  # Commit to generate the user_id


user_1 = User(
    name="divya",
    email="divya@test.com",
    mobile="8248831127",
    password="admin@123",
    age=27,
    gender="M",
    role="user"
)
session.add(user_1)
session.commit() 



# Step 2: Insert data into the strategy table (Parent)
strategy_1 = Strategy(
    strategy_name="3ema",
    uuid="123qwe",
    created_at=datetime(2025, 4, 24, 9, 4, 59),
    updated_at=datetime(2025, 4, 24, 9, 4, 59),
    created_by=1,
    is_deleted=False
)
session.add(strategy_1)
session.commit()  # Commit to generate the strategy ID

# Step 3: Insert data into the stock_details table (Parent)
# stock_detail_1 = StockDetails(
#     stock_name="FINNIFTY",
#     token="99926037",
#     ltp=26036.1,
#     last_update=datetime(2025, 4, 25, 22, 24, 27, 988122)
# )


# stock_detail_1 = StockDetails(
#     stock_name="FINNIFTY",
#     token="99926037",
#     ltp=26036.1,
#     last_update=datetime(2025, 4, 25, 22, 24, 27, 988122)
# )

# stock_detail_1 = StockDetails(
#     stock_name="FINNIFTY",
#     token="99926037",
#     ltp=26036.1,
#     last_update=datetime(2025, 4, 25, 22, 24, 27, 988122)
# )
# session.add(stock_detail_1)
# session.commit()  # Commit to generate the stock_token

# Step 4: Insert data into the login_track table (Child)
# login_track_1 = LoginTrack(
#     user_id=user_1.id,  # Reference to the user inserted earlier
#     token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6InZlZXJhQHRlc3QuY29tIiwiZXhwIjoxNzQ1NzEyOTk5fQ.ElUtwiKYyfgo8ycWzt8Zn3KUeimsVubqLUCh_CmAwjY",
#     login_time=datetime(2025, 4, 26, 12, 16, 39, 673547),
#     ip_address="0.0.0.0",
#     device_info="Unknown Device"
# )
# session.add(login_track_1)
# session.commit()  # Commit the login track

# Step 5: Insert data into the user_active_strategy table (Child)
user_active_strategy_1 = UserActiveStrategy(
    user_id=user_1.id,  # Reference to the user inserted earlier
    strategy_id="123qwe",  # Reference to the strategy inserted earlier
    stock_token="99926037",  # Reference to the stock token inserted earlier
    trade_count=2,
    quantity=3,
    paper_trade=True,
    created_at=datetime(2025, 4, 24, 9, 4, 59),
    updated_at=datetime(2025, 4, 24, 9, 4, 59),
    is_active=True,
    is_started=False,
    status="close"
)
session.add(user_active_strategy_1)
session.commit()  # Commit to generate the user_active_strategy_id

# Step 6: Insert data into the order_manager table (Child)
order_manager_1 = OrderManager(
    order_id="test1",
    completed_order_count=1,
    buy_count=2,
    sell_count=0,
    is_active=True,
    created_at=datetime(2025, 4, 24, 9, 4, 59),
    updated_at=datetime(2025, 4, 24, 9, 4, 59),
    user_active_strategy_id=user_active_strategy_1.id  # Reference to the user active strategy inserted earlier
)
session.add(order_manager_1)
session.commit()  # Commit to generate order manager ID

# Step 7: Insert data into the equity_trade_history table (Child)
equity_trade_history_1 = EquityTradeHistory(
    order_id="test1",
    stock_token="99926037",  # Reference to the stock token inserted earlier
    trade_type="buy",
    quantity=3,
    price=400,
    entry_ltp=400,
    exit_ltp=600,
    total_price=1200,
    trade_entry_time=datetime(2025, 4, 25, 22, 24, 27, 988),
    trade_exit_time=datetime(2025, 4, 25, 22, 24, 27, 988)
)
session.add(equity_trade_history_1)
session.commit()  # Commit the trade history

# Close the session
session.close()

print("Data inserted successfully")

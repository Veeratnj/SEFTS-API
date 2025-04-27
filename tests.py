from app.models.models import StockDetails
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database URL (you can modify this as per your actual database)
DATABASE_URL = "postgresql://setc:admin%40123@localhost/setc"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Data to be inserted into the stock_details table
stock_details_data = [
    {"stock_name": "FINNIFTY", "token": "99926037", "ltp": 26036.1, "last_update": datetime(2025, 4, 25, 22, 24, 27, 988122)},
    {"stock_name": "NIFTY50", "token": "99926000", "ltp": 24039.35, "last_update": datetime(2025, 4, 25, 22, 24, 27, 991000)},
    {"stock_name": "BANKNIFTY", "token": "99926009", "ltp": 54664.05, "last_update": datetime(2025, 4, 25, 22, 24, 27, 992000)},
    {"stock_name": "SBIN-EQ", "token": "3045", "ltp": 8500.0, "last_update": datetime(2025, 4, 25, 22, 24, 27, 994000)},
    {"stock_name": "ABAN-EQ", "token": "10", "ltp": 200.0, "last_update": datetime(2025, 4, 25, 22, 24, 27, 994500)},
    {"stock_name": "ADANIENT-EQ", "token": "25", "ltp": 400.08, "last_update": datetime(2025, 4, 25, 22, 24, 27, 994600)},
    {"stock_name": "BHEL-EQ", "token": "438", "ltp": 590.65, "last_update": datetime(2025, 4, 25, 22, 24, 27, 994700)},
]

# Insert each row of stock details into the table
for stock in stock_details_data:
    stock_detail = StockDetails(
        stock_name=stock["stock_name"],
        token=stock["token"],
        ltp=stock["ltp"],
        last_update=stock["last_update"]
    )
    session.add(stock_detail)

# Commit the changes to the database
session.commit()

# Close the session
session.close()

print("Stock details inserted successfully")

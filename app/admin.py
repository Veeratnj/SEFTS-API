# admin.py

from sqladmin import Admin, ModelView
from fastapi import FastAPI
from app.db.db import engine  # your engine
from app.models.models import BankNiftyOptionsTradeHistory, OptionKillStatus, User, Strategy, StockDetails, UserActiveStrategy, OrderManager, EquityTradeHistory, LoginTrack,Stocks

# Admin Views
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.email, User.role]
    column_searchable_list = [User.name, User.email]

class StrategyAdmin(ModelView, model=Strategy):
    column_list = [Strategy.id, Strategy.strategy_name, Strategy.uuid, Strategy.created_at]

class StockDetailsAdmin(ModelView, model=StockDetails):
    column_list = [StockDetails.id, StockDetails.stock_name, StockDetails.token, StockDetails.ltp]

class UserActiveStrategyAdmin(ModelView, model=UserActiveStrategy):
    column_list = [UserActiveStrategy.id, UserActiveStrategy.user_id, UserActiveStrategy.strategy_id, UserActiveStrategy.status]

class OrderManagerAdmin(ModelView, model=OrderManager):
    column_list = [OrderManager.id, OrderManager.order_id, OrderManager.is_active]

class EquityTradeHistoryAdmin(ModelView, model=EquityTradeHistory):
    column_list = [EquityTradeHistory.id, EquityTradeHistory.order_id, EquityTradeHistory.trade_type, EquityTradeHistory.quantity, EquityTradeHistory.price]

class LoginTrackAdmin(ModelView, model=LoginTrack):
    column_list = [LoginTrack.id, LoginTrack.user_id, LoginTrack.login_time, LoginTrack.logout_time, LoginTrack.ip_address]


class StocksAdmin(ModelView, model=Stocks):
    column_list = [Stocks.id, Stocks.stock_name, Stocks.token, Stocks.exchange, Stocks.is_hotlist, Stocks.trend_type, Stocks.created_at, Stocks.updated_at, Stocks.created_by, Stocks.is_deleted]

class BankNiftyOptionsTradeHistoryAdmin(ModelView, model=BankNiftyOptionsTradeHistory):
    column_list = [
        BankNiftyOptionsTradeHistory.id,
        BankNiftyOptionsTradeHistory.order_id,
        BankNiftyOptionsTradeHistory.option_symbol,
        BankNiftyOptionsTradeHistory.option_type,
        BankNiftyOptionsTradeHistory.trade_type,
        BankNiftyOptionsTradeHistory.quantity,
        BankNiftyOptionsTradeHistory.entry_ltp,
        BankNiftyOptionsTradeHistory.exit_ltp,
        BankNiftyOptionsTradeHistory.entry_price,
        BankNiftyOptionsTradeHistory.exit_price,
        BankNiftyOptionsTradeHistory.trade_entry_time,
        BankNiftyOptionsTradeHistory.trade_exit_time,
    ]
    column_searchable_list = [BankNiftyOptionsTradeHistory.order_id, BankNiftyOptionsTradeHistory.option_symbol]
    column_sortable_list = [BankNiftyOptionsTradeHistory.trade_entry_time, BankNiftyOptionsTradeHistory.trade_exit_time]

class OptionKillStatusAdmin(ModelView, model=OptionKillStatus):
    column_list = [OptionKillStatus.id, OptionKillStatus.is_closed]





# Attach to app
def setup_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(StrategyAdmin)
    admin.add_view(StockDetailsAdmin)
    admin.add_view(UserActiveStrategyAdmin)
    admin.add_view(OrderManagerAdmin)
    admin.add_view(EquityTradeHistoryAdmin)
    admin.add_view(LoginTrackAdmin)
    admin.add_view(StocksAdmin)
    admin.add_view(BankNiftyOptionsTradeHistoryAdmin)
    admin.add_view(OptionKillStatusAdmin)

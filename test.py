# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp
from logzero import logger
import pandas as pd
import app.credentials.creds as creds

api_key = creds.api_key
username = creds.username
pwd = creds.pwd
smartApi = SmartConnect(api_key)
try:
    token = creds.token
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)


#data['data'] = ['clientcode', 'name', 'email', 'mobileno', 'exchanges', 'products', 'lastlogintime', 'broker', 'jwtToken', 'refreshToken', 'feedToken']

print((data['data'].keys()))



params = {
    "exchange": "NSE",
    "symboltoken": "11536",  
    "interval": "FIVE_MINUTE",  
    "fromdate": "2024-04-04 09:15",  
    "todate": "2024-04-04 15:30"
}

response = smartApi.getCandleData(params)

if 'data' in response:
    df = pd.DataFrame(response['data'], columns=["datetime", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    print(df.head())
else:
    print("❌ Error fetching candle data:", response)
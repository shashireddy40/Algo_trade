import pandas as pd
import sqlite3
from tabulate import tabulate


con = sqlite3.connect("banknifty.db")

query = 'select * from banknifty2023'
df = pd.read_sql_query(query,con)

df["datetime"] = pd.to_datetime(df['datetime'])
df.set_index(keys='datetime', inplace= True)

df_3min = df.resample('3T').agg({
    'stock_code': 'first',
    'exchange_code': 'first',
    'product_type': 'first',
    'expiry_date': 'first',
    'right': 'first',
    'strike_price': 'first',
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum',
    'open_interest': 'last',
    'count': 'sum'
})

df_5min = df.resample('5T').agg({
    'stock_code': 'first',
    'exchange_code': 'first',
    'product_type': 'first',
    'expiry_date': 'first',
    'right': 'first',
    'strike_price': 'first',
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'volume': 'sum',
    'open_interest': 'last',
    'count': 'sum'
})

df_3min.reset_index(inplace=True)
df_5min.reset_index(inplace=True)



print(tabulate(df_3min.head(5),headers='keys',tablefmt="psql"))
con.close()






# def oipluse_buy_and_sell():
#     for script in script_list:
#         data = {
#             "symbol": f"{exchange}:{script}",
#             "resolution": timeframe,
#             "date_format": "1",
#             "range_from": from_date,
#             "range_to": today,
#             "cont_flag": "0",
#         }
#         try:
#             hist_data = fyers.history(data)
#         except Exception as e:
#             raise e
#         df = pd.DataFrame(
#             hist_data["candles"],
#             columns=["date", "open", "high", "low", "close", "volume"],
#         )
#         df["date"] = pd.to_datetime(df["date"], unit="s", utc=True)
#         df["date"] = df["date"].dt.tz_convert("Asia/Kolkata")

#         # Extract the time component
#         df["time"] = df["date"].dt.time

#         # Calculate RSI
#         df["rsi"] = ta.RSI(df["close"], timeperiod=14).round(2)

#         # Calculate VWMA
#         df["vwma"] = ta.SMA(df["close"] * df["volume"], timeperiod=14) / df["volume"]

#         # Calculate VWAP manually
#         df["vwap"] = calculate_vwap(df)

#         # Initialize variables
#         consecutive_count = 0
#         selected_indices = []

#         for i in range(2, len(df)):
#             time = df["time"][i]

#             if (
#                 df["volume"][i - 2] > 50000
#                 and df["volume"][i - 1] > 50000
#                 and df["rsi"][i] > 50
#                 and df["close"][i] > df["vwap"][i]
#                 and df["close"][i] > df["vwma"][i]
#                 and datetime.time(10, 0)
#                 <= time
#                 <= datetime.time(15, 0)  # Time between 10 AM and 3 PM
#             ):
#                 if consecutive_count == 0:
#                     # Buy condition: place a buy order
#                     placeOrder(script, "BUY")
#                     print("Buy Order Placed")
#                 consecutive_count += 1
#             elif (
#                 # Additional selling condition
#                 consecutive_count > 0
#                 and df["close"][i] < df["vwap"][i]  # There was a prior buy condition
#                 and df["close"][i] < df["vwma"][i]
#             ):
#                 # Sell condition: place a sell order
#                 placeOrder(script, "SELL")
#                 print("Sell Order Placed")
#                 break  # Exit the loop after placing the sell order
#         print("oipluse")
#         return df
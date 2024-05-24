import yaml
import urllib
import json
import datetime as dt
from datetime import datetime
import pytz
import pandas as pd

timezone = pytz.timezone('Asia/Kolkata')

def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def fetch_instrument_list(url):
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

def get_trading_details(obj, searchscrip, exchange):
    script = obj.searchScrip(exchange=exchange, searchscrip=searchscrip)
    symboltoken = script['data'][0]['symboltoken']
    tradingsymbol = script['data'][0]['tradingsymbol']
    return symboltoken, tradingsymbol

def get_option_symbol(ltp, expiry_dates, ticker, strike, signal):
    expiry_date = [datetime.strptime(date, "%d-%b-%Y").strftime("%d%b%y").upper() for date in expiry_dates]
    strike = int(round(ltp, -2) + strike) if signal == 'CE' else int(round(ltp, -2) - strike)

    try:
        date_objects = [datetime.strptime(date_str, "%d%b%y") for date_str in expiry_date]
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        upcoming_date = min((date for date in date_objects if date >= current_date), default=None)
        token_expiry = upcoming_date.strftime("%d%b%y").upper()
    except ValueError as e:
        print(f"Error: {e}")
        return None

    derivative = f'{ticker}{token_expiry}{strike}{signal}'
    print(f'We are trading on {derivative}')
    return derivative

def token_lookup(ticker, instrument_list, exchange='NFO'):
    fut_symbol = 'MAY24FUT'
    if exchange == 'NFO':
        for instrument in instrument_list:
            if (
                instrument["name"] == ticker
                and instrument["exch_seg"] == exchange
                and instrument["symbol"][-8:] == fut_symbol
            ):
                return instrument["token"]
    else:
        for instrument in instrument_list:
            if (
                instrument["name"] == ticker
                and instrument["exch_seg"] == exchange
                and instrument["symbol"] == 'Nifty Bank'
            ):
                return instrument["token"]
    return 'no token'

def option_token(ticker, instrument_list, exchange='NFO'):
    for instrument in instrument_list:
        if instrument["symbol"] == ticker and instrument["exch_seg"] == exchange:
            return instrument["token"]

def symbol_lookup(token, instrument_list, exchange='NFO'):
    fut_symbol = 'MAY24FUT'
    for instrument in instrument_list:
        if (
            instrument["token"] == token
            and instrument["exch_seg"] == exchange
            and instrument["symbol"][-8:] == fut_symbol
        ):
            return instrument["name"]

def get_ltp(obj, symbol, token, exchange='NFO'):
    response = obj.ltpData(exchange, symbol, token)
    return response["data"]["ltp"]

def place_market_order(obj, tradingsymbol, symboltoken, transactiontype, quantity, exchange='NFO'):
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": tradingsymbol,
        "symboltoken": symboltoken,
        "transactiontype": transactiontype,
        "exchange": exchange,
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "quantity": quantity
    }
    orderId = obj.placeOrder(orderparams)
    print(orderparams)
    print(f"placing market order with {quantity} at {datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')} with {orderId}")
    return orderId

def place_stoploss_order(obj, tradingsymbol, symboltoken, quantity, stoploss, exchange='NFO'):
    orderparams = {
            "variety": "STOPLOSS",
            "tradingsymbol": tradingsymbol,
            "symboltoken": symboltoken,
            "transactiontype": "SELL",
            "exchange": exchange,
            "ordertype": "STOPLOSS_LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": stoploss-1,
            "triggerprice": stoploss,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": quantity
            }
    orderId = obj.placeOrder(orderparams)
    print(orderparams)
    print(f"placing stop loss order at {datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')} with {orderId}")
    return orderId

def modify_order(obj, orderid, buyprice, quantity, tradingsymbol, symboltoken, exchange="NFO"):
    if requiredvalue(obj, orderid, "orderstatus") == 'trigger pending':
        orderparams = {
        "variety":"STOPLOSS",
        "orderid":orderid,
        "ordertype":"STOPLOSS_LIMIT",
        "producttype":"INTRADAY",
        "duration":"DAY",
        "price":buyprice-2,
        "triggerprice": buyprice,
        "quantity":quantity,
        "tradingsymbol":tradingsymbol,
        "symboltoken":symboltoken,
        "exchange":exchange
        }
        status = obj.modifyOrder(orderparams)
        print(orderparams)
        print(f"modifying the stop loss order at {datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')} with {status}")
    else:
        print(f"{orderid} is closed already)")
    return status

def requiredvalue(obj, orderid, outputvalue):
    retry_count = 0
    while retry_count < 5:
        try:
            for order in obj.orderBook()['data']:
                if order['orderid'] == orderid:
                    return order[outputvalue]
        except Exception as e:
            print(f"Error occurred: {e}")
            retry_count += 1
            print(f"Retrying... Attempt at requiredvalue func {retry_count}")
            time.sleep(3)
    return None

import time
import datetime as dt
from datetime import datetime
import pytz
import helpers
import login
import strategy

def main():
    config_path = "/Users/shashi/Documents/quantala_projects/algo_trade/config/config.yml"
    instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    tickers = ["BANKNIFTY"]
    future_expiry = "BANKNIFTY29MAY24FUT"
    quantity = 15
    first_buy_quantity = 45
    expiry_dates = [
    "03-Apr-2024",
    "10-Apr-2024",
    "24-Apr-2024",
    "30-Apr-2024",
    "08-May-2024",
    '15-May-2024', 
    '22-May-2024', 
    '29-May-2024', 
    '05-Jun-2024', 
    '26-Jun-2024', # update dates on weekly expiry (need to automate from NSE)
    '27-Jun-2024', 
    '31-Jul-2024', 
    '25-Sep-2024', 
    '26-Sep-2024', 
    '24-Dec-2024']

    monthly_expiry = ["24-Apr-2024",
                    "29-May-2024", 
                    "26-Jun-2024",
                    "25-Sep-2024",
                    "24-Dec-2024"]

    monthly_expiry_FUT = ["24APR24FUT",
                    "29May24FUT", 
                    "26Jun24FUT",
                    "25Sep24FUT",
                    "24Dec24FUT"]

    obj, authToken, refreshToken, feedToken, res = login.login(config_path)
    instrument_list = helpers.fetch_instrument_list(instrument_url)

    print("9:20 candle")
    start_time_9_20 = dt.datetime.now(helpers.timezone).replace(hour=9, minute=30, second=0, microsecond=0)
    current_time = dt.datetime.now(helpers.timezone).replace(microsecond=0)
    if current_time < start_time_9_20:
        time_difference = start_time_9_20 - current_time
        print(f'sleeping {time_difference}')
        time.sleep(time_difference.total_seconds())
        print(f"My time: {dt.datetime.now(helpers.timezone).strftime('%Y-%m-%d %H:%M')}")
        print('Start my program')
        data_0920 = strategy.hist_data_0920(obj, tickers, "FIFTEEN_MINUTE", instrument_list)

    data_0920 = strategy.hist_data_0920(obj, tickers, "FIFTEEN_MINUTE", instrument_list)
    start_time_9_21 = dt.datetime.now(helpers.timezone).replace(hour=9, minute=33, second=0, microsecond=0)
    rightnow = dt.datetime.now(helpers.timezone).replace(microsecond=0)
    if rightnow < start_time_9_21:
        time_difference = start_time_9_21 - rightnow
        print(f'sleeping {time_difference}')
        time.sleep(time_difference.total_seconds())
        print(f"My time: {dt.datetime.now(helpers.timezone).strftime('%Y-%m-%d %H:%M')}")
        print('streaming_3_min_data')

    while True:
        start_execution_time = time.time()
        strategy.fiftien_min_strategy(obj, tickers, first_buy_quantity, quantity, instrument_list, expiry_dates, data_0920, future_expiry)
        end_execution_time = time.time()
        execution_time = end_execution_time - start_execution_time
        sleep_time = max(0, 1 * 2 - execution_time)
        print(dt.datetime.now(helpers.timezone).strftime('%Y-%m-%d %H:%M'))
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()

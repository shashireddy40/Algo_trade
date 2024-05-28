import time
import datetime as dt
from datetime import datetime
import pandas as pd
import helpers
import indicator

def hist_data_0920(obj, tickers, interval, instrument_list, exchange="NFO"):
    print("getting the 9:20 candle")
    hist_data_tickers = {}
    for ticker in tickers:
        time.sleep(1)
        params = {
                 "exchange": exchange,
                 "symboltoken": helpers.token_lookup(ticker, instrument_list, exchange),
                 "interval": interval,
                 "fromdate": dt.date.today().strftime('%Y-%m-%d') + ' 09:15',
                 "todate": dt.date.today().strftime('%Y-%m-%d') + ' 09:20'
                 }
        print(params)
        hist_data = obj.getCandleData(params)
        df_data = pd.DataFrame(hist_data["data"],
                               columns = ["date","open","high","low","close","volume"])
        df_data.set_index("date",inplace=True)
        df_data.index = pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        hist_data_tickers[ticker] = df_data
        high_first_5_min = df_data['high']
        low_first_5_min = df_data['low']
        high = high_first_5_min.iloc[-1]
        low = low_first_5_min.iloc[-1]
    print(high, low)
    return high, low

def fiftien_min_strategy(obj, tickers, first_buy_quantity, quantity, instrument_list, expiry_dates, data_0920, future_expiry, exchange="NFO"):
    five_buy_scrpit = []
    for ticker in tickers:
        time.sleep(2)
        params = {
            "exchange": exchange,
            "symboltoken": helpers.token_lookup(ticker, instrument_list),
            "interval": "THREE_MINUTE",
            "fromdate": (dt.date.today() - dt.timedelta(days=4)).strftime('%Y-%m-%d') + ' 02:30',
            "todate": dt.datetime.now(helpers.timezone).strftime('%Y-%m-%d %H:%M')
        }
        retry_count = 0
        while retry_count < 5:
            try:
                hist_data = obj.getCandleData(params)
                df_data = pd.DataFrame(hist_data["data"],
                                       columns=["date", "open", "high", "low", "close", "volume"])
                df_data.set_index("date", inplace=True)
                df_data.index = pd.to_datetime(df_data.index)
                df_data.index = df_data.index.tz_localize(None)
                df_data['RSI'] = indicator.calculate_rsi(df_data)
                print(df_data.tail(5))
                if df_data["close"].iloc[-2] > int(round(data_0920[0], -1)) and df_data['RSI'].iloc[-2] < 70:
                    future_price = helpers.get_ltp(obj, future_expiry, helpers.option_token(future_expiry, instrument_list))
                    BULL = helpers.get_option_symbol(future_price, expiry_dates, tickers[0], -100, "CE")
                    bull_token = helpers.option_token(BULL, instrument_list, exchange='NFO')
                    time.sleep(5)
                    print("We are on trade")
                    if len(five_buy_scrpit) == 0:
                        print(f'we are buying {BULL}')
                        first_orderid = helpers.place_market_order(obj, BULL, bull_token, "BUY", first_buy_quantity, exchange='NFO')
                        five_buy_scrpit.append(BULL)
                        option_data = {
                            "exchange": "NFO",
                            "symboltoken": bull_token,
                            "interval": "FIFTEEN_MINUTE",
                            "fromdate": dt.date.today().strftime('%Y-%m-%d') + ' 09:15',
                            "todate": dt.date.today().strftime('%Y-%m-%d') + ' 09:20'
                        }
                        candle_data = obj.getCandleData(option_data)
                        first_sl = candle_data['data'][0][3]
                        second_sl = (int(candle_data['data'][0][3]) + int(candle_data['data'][0][2])) / 2
                        current_time = datetime.now(helpers.timezone)
                        timenow = current_time.strftime('%Y-%m-%d %H:%M:%S')
                        time.sleep(3)
                        First_SL_order_id = helpers.place_stoploss_order(obj, BULL, helpers.option_token(BULL, instrument_list, exchange='NFO'), quantity, first_sl)
                        time.sleep(2)
                        Second_SL_order_id = helpers.place_stoploss_order(obj, BULL, helpers.option_token(BULL, instrument_list, exchange='NFO'), quantity, second_sl)
                        time.sleep(2)
                        Third_SL_order_id = helpers.place_stoploss_order(obj, BULL, helpers.option_token(BULL, instrument_list, exchange='NFO'), quantity, second_sl)
                        time.sleep(2)
                        message = f"CE bought {first_buy_quantity} stocks of {BULL} at {timenow} with first sl of  {first_sl} and second sl {second_sl}"
                        with open("tradebook24APR.txt", "a") as file:
                            file.write(message + "\n")
                    else:
                        print("we are already in SELL SIDE")
                elif df_data["close"].iloc[-2] < int(round(data_0920[1], -1)) and df_data['RSI'].iloc[-2] > 30:
                    future_price = helpers.get_ltp(obj, future_expiry, helpers.option_token(future_expiry, instrument_list))
                    time.sleep(2)
                    BEAR = helpers.get_option_symbol(future_price, expiry_dates, tickers[0], 300, "PE")
                    time.sleep(3)
                    bear_token = helpers.option_token(BEAR, instrument_list, exchange='NFO')
                    time.sleep(2)
                    if len(five_buy_scrpit) == 0:
                        time.sleep(5)
                        first_orderid = helpers.place_market_order(obj, BEAR, bear_token, "BUY", first_buy_quantity, exchange='NFO')
                        time.sleep(2)
                        five_buy_scrpit.append(BEAR)
                        current_time = datetime.now(helpers.timezone)
                        timenow = current_time.strftime('%Y-%m-%d %H:%M:%S')
                        time.sleep(3)
                        option_data = {
                            "exchange": "NFO",
                            "symboltoken": bear_token,
                            "interval": "FIFTEEN_MINUTE",
                            "fromdate": dt.date.today().strftime('%Y-%m-%d') + ' 09:15',
                            "todate": dt.date.today().strftime('%Y-%m-%d') + ' 09:20'
                        }
                        candle_data = obj.getCandleData(option_data)
                        time.sleep(2)
                        first_sl = (int(candle_data['data'][0][3]) + int(candle_data['data'][0][2])) / 2
                        second_sl = (int(candle_data['data'][0][3]) + int(candle_data['data'][0][2])) / 2
                        First_SL_order_id = helpers.place_stoploss_order(obj, BEAR, bear_token, quantity, first_sl)
                        time.sleep(2)
                        Second_SL_order_id = helpers.place_stoploss_order(obj, BEAR, bear_token, quantity, second_sl)
                        time.sleep(1)
                        Third_SL_order_id = helpers.place_stoploss_order(obj, BEAR, bear_token, quantity, second_sl)
                        message = f"PE bought {quantity} stocks of {BEAR} at {timenow} with first sl of  {first_sl} and second sl {second_sl}"
                        with open("tradebook24APR.txt", "a") as file:
                            file.write(message + "\n")
                    else:
                        print("we are already in SELL SIDE")
                break
            except Exception as e:
                print(f"Error occurred: {e}")
                retry_count += 1
                print(f"Retrying... Attempt {retry_count}")
                time.sleep(5)
    if len(five_buy_scrpit) > 0:
        first_buy_price, first_buy_quantity, tradingsymbol, symboltoken = helpers.get_order_details(obj, first_orderid)
        while True:
            list_of_orders = [First_SL_order_id, Second_SL_order_id, Third_SL_order_id]
            exit_all_loops = False
            half_quantity = 15

            margins = [0.10, 0.1667, 0.3333, 0.5, 0.6667, 0.8333, 1.0, 1.1667, 1.5, 1.6667, 2.0, 2.3333, 2.6667, 3.0, 3.3333]
            sl_values = {
                0.10: (0.0667, 0.0333),
                0.1667: 0.1,
                0.3333: 0.2667,
                0.5: (0.4, 0.4667),
                0.6667: 0.5,
                0.8333: 0.6667,
                1.0: 0.8333,
                1.1667: 1.0,
                1.5: 1.1667,
                1.6667: 1.5,
                2.0: 1.8333,
                2.3333: 2.1667,
                2.6667: 2.5,
                3.0: 2.8333,
                3.3333: 3.3
            }

            for margin in margins:
                if exit_all_loops:
                    break
                while True:
                    if exit_all_loops:
                        break
                    print(f"checking {margin * 100}% profit")
                    if helpers.requiredvalue(obj, First_SL_order_id if margin in [0.10, 0.3333, 0.6667, 1.0, 1.5, 2.0, 2.6667, 3.3333] else Second_SL_order_id, "orderstatus") == 'trigger pending':
                        time.sleep(2)
                        if (first_buy_price * margin) <= (helpers.get_ltp(obj, tradingsymbol, symboltoken) - first_buy_price):
                            if margin == 0.10:
                                sl, sl3 = sl_values[margin]
                                helpers.modify_order(obj, First_SL_order_id, first_buy_price * (1 + sl), half_quantity, tradingsymbol, symboltoken)
                                helpers.modify_order(obj, Third_SL_order_id, first_buy_price * (1 + sl3), half_quantity, tradingsymbol, symboltoken)
                                helpers.modify_order(obj, Second_SL_order_id, first_buy_price * (1 + sl3), half_quantity, tradingsymbol, symboltoken)
                            elif margin == 0.5:
                                sl, sl3 = sl_values[margin]
                                helpers.modify_order(obj, Second_SL_order_id, first_buy_price * (1 + sl), half_quantity, tradingsymbol, symboltoken)
                                helpers.modify_order(obj, Third_SL_order_id, first_buy_price * (1 + sl3), half_quantity, tradingsymbol, symboltoken)
                            elif margin == 3.3333:
                                sl = sl_values[margin]
                                helpers.modify_order(obj, First_SL_order_id, first_buy_price * (1 + sl), half_quantity, tradingsymbol, symboltoken)
                                helpers.modify_order(obj, Second_SL_order_id, first_buy_price * (1 + sl), half_quantity, tradingsymbol, symboltoken)
                                order_status = helpers.get_order_status(obj, list_of_orders)
                                if all(order_status[order] == 'complete' for order in list_of_orders):
                                    exit_all_loops = True
                                    break
                            else:
                                sl = sl_values[margin]
                                helpers.modify_order(obj, First_SL_order_id if margin in [0.10, 0.3333, 0.6667, 1.0, 1.5, 2.0, 2.6667, 3.3333] else Second_SL_order_id, first_buy_price * (1 + sl), half_quantity, tradingsymbol, symboltoken)
                            print("modified")
                            time.sleep(5)
                            break
                    else:
                        print(f'this is my {helpers.getpnl(obj)}')
                        time.sleep(2)
                        order_status = helpers.get_order_status(obj, list_of_orders)
                        if all(order_status[order] == 'complete' for order in list_of_orders):
                            time.sleep(5)
                            exit_all_loops = True
                            break
            print(f'today is final profit {helpers.getpnl(obj)}')

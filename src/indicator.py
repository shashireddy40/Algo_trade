import pandas as pd
import talib

def calculate_rsi(df, period=14):
    rsi = talib.RSI(df['close'], timeperiod=period)
    return rsi

def calculate_vwma(df, period=14):
    pv = df['close'] * df['volume']
    vwma = pv.rolling(window=period).sum() / df['volume'].rolling(window=period).sum()
    return vwma

def calculate_vwap(df):
    vwap = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    return vwap

def calculate_bollinger_bands(df, period=20, nbdevup=2, nbdevdn=2, matype=0):
    upperband, middleband, lowerband = talib.BBANDS(df['close'], timeperiod=period, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
    return upperband, middleband, lowerband

def calculate_ma(df, period=20):
    ma = talib.SMA(df['close'], timeperiod=period)
    return ma

def calculate_supertrend(df, period=7, multiplier=3):
    atr = talib.ATR(df['high'], df['low'], df['close'], timeperiod=period)
    hl2 = (df['high'] + df['low']) / 2
    basic_upperband = hl2 + (multiplier * atr)
    basic_lowerband = hl2 - (multiplier * atr)
    final_upperband = basic_upperband.copy()
    final_lowerband = basic_lowerband.copy()

    for i in range(1, len(df)):
        final_upperband[i] = min(basic_upperband[i], final_upperband[i-1]) if df['close'][i-1] > final_upperband[i-1] else basic_upperband[i]
        final_lowerband[i] = max(basic_lowerband[i], final_lowerband[i-1]) if df['close'][i-1] < final_lowerband[i-1] else basic_lowerband[i]

    supertrend = pd.Series(0, index=df.index)
    for i in range(1, len(df)):
        if df['close'][i] > final_upperband[i-1]:
            supertrend[i] = final_lowerband[i]
        elif df['close'][i] < final_lowerband[i-1]:
            supertrend[i] = final_upperband[i]
        else:
            supertrend[i] = supertrend[i-1]

    return supertrend

def calculate_macd(df, fastperiod=12, slowperiod=26, signalperiod=9):
    macd, signal, hist = talib.MACD(df['close'], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, signal, hist

def calculate_pivot_points(df):
    pivot = (df['high'] + df['low'] + df['close']) / 3
    r1 = (2 * pivot) - df['low']
    s1 = (2 * pivot) - df['high']
    r2 = pivot + (df['high'] - df['low'])
    s2 = pivot - (df['high'] - df['low'])
    r3 = df['high'] + 2 * (pivot - df['low'])
    s3 = df['low'] - 2 * (df['high'] - pivot)
    return pivot, r1, s1, r2, s2, r3, s3

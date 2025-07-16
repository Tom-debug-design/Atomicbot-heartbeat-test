import pandas as pd
import requests
from indicator_tools import calculate_rsi, calculate_ema
from holdings_tracker import check_sell_conditions
from learner import get_token_priority

TOKENS = [
    'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT',
    'SOLUSDT', 'AVAXUSDT', 'MATICUSDT', 'DOGEUSDT', 'DOTUSDT',
    'LINKUSDT', 'LTCUSDT', 'NEARUSDT', 'ATOMUSDT', 'ARBUSDT',
    'APTUSDT', 'OPUSDT', 'FTMUSDT', 'INJUSDT', 'RNDRUSDT'
]
TRADE_SIZE = 50  # USD per trade

def fetch_ohlcv(symbol, interval="1m", limit=50):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=["time", "open", "high", "low", "close", "volume", "_", "_", "_", "_", "_"])
    df["close"] = pd.to_numeric(df["close"])
    return df

def generate_trades():
    trades = []
    priorities = get_token_priority(TOKENS)
    for symbol in priorities:
        try:
            df = fetch_ohlcv(symbol)
            df["rsi"] = calculate_rsi(df["close"])
            df["ema9"] = calculate_ema(df["close"], 9)
            df["ema21"] = calculate_ema(df["close"], 21)

            latest = df.iloc[-1]
            prev = df.iloc[-2]

            # BUY-signal
            if latest["rsi"] < 30 and prev["ema9"] < prev["ema21"] and latest["ema9"] > latest["ema21"]:
                price = latest["close"]
                qty = round(TRADE_SIZE / price, 6)
                trades.append({
                    "symbol": symbol,
                    "price": price,
                    "qty": qty,
                    "message": f"🚀 BUY {symbol} at ${price:.2f} | RSI: {latest['rsi']:.1f}"
                })
            # SELL-signal
            sell_msg = check_sell_conditions(symbol, latest["close"], latest["rsi"])
            if sell_msg:
                trades.append({"symbol": symbol, "price": latest["close"], "qty": 0, "message": sell_msg})
        except Exception as e:
            print(f"Strategy error on {symbol}: {e}")
    return trades

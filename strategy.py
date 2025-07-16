import requests
import random

TOKENS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT', 'AVAXUSDT', 'MATICUSDT']
USDT_BALANCE = 1000
TRADE_SIZE_PERCENT = 5

def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    return float(response.json()['price'])

def fake_rsi():
    return random.randint(10, 90)

def fake_ema_cross():
    return random.choice([True, False])

def check_buy_signal():
    triggered = []
    for symbol in TOKENS:
        try:
            price = fetch_price(symbol)
            rsi = fake_rsi()
            ema_cross = fake_ema_cross()
            if rsi < 30 and ema_cross:
                amount = USDT_BALANCE * (TRADE_SIZE_PERCENT / 100)
                qty = round(amount / price, 6)
                msg = f"🚀 Aggressive BUY: {symbol} at ${price:,.2f} | Qty: {qty} | RSI: {rsi}"
                triggered.append({"symbol": symbol, "price": price, "qty": qty, "message": msg})
        except Exception as e:
            print(f"Strategy error on {symbol}: {e}")
    return triggered

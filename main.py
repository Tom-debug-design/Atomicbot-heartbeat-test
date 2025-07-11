import requests
import time
from flask import Flask
from threading import Thread
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"
BALANCE_USDT = 1000  # Simulated total capital
TRADE_PERCENT = 0.05  # 5% per trade

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT"]

def send_discord_message(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("Discord error:", e)

def fetch_price(symbol):
    try:
        res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        return float(res.json()['price'])
    except Exception as e:
        print(f"Failed to fetch price for {symbol}: {e}")
        return None

def simulate_trade():
    while True:
        for symbol in SYMBOLS:
            price = fetch_price(symbol)
            if price:
                usdt_amount = BALANCE_USDT * TRADE_PERCENT
                quantity = round(usdt_amount / price, 6)
                now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                msg = f"💰 Simulated BUY: {symbol} at ${price:.2f} | Amount: ${usdt_amount:.2f} | Qty: {quantity} (UTC: {now})"
                send_discord_message(msg)
            time.sleep(5)
        time.sleep(3600 - 5 * len(SYMBOLS))  # One full cycle every hour

@app.route("/")
def home():
    return "Live-price 5% simulation running."

def run_scheduler():
    t = Thread(target=simulate_trade)
    t.daemon = True
    t.start()

if __name__ == "__main__":
    run_scheduler()
    app.run(host="0.0.0.0", port=5000)

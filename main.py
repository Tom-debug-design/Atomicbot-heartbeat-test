
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"
TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT"]
TRADE_INTERVAL = 60  # seconds
HEARTBEAT_INTERVAL = 3600  # seconds

def send_to_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Failed to send message to Discord: {e}")

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def simulate_trades():
    balance = 1000  # Simulert USDT balanse
    amount = balance * 0.05
    for symbol in TOKENS:
        price = get_price(symbol)
        if price:
            qty = amount / price
            message = f"💰 Simulated BUY: {symbol} at ${price:.2f} | Amount: ${amount:.2f} | Qty: {qty:.4f}"
            print(message)
            send_to_discord(message)

def trade_loop():
    while True:
        simulate_trades()
        time.sleep(TRADE_INTERVAL)

def heartbeat_loop():
    hour_count = 0
    while True:
        hour_count += 1
        message = f"⏰ Hourly report: {hour_count}/24 completed."
        print(message)
        send_to_discord(message)
        time.sleep(HEARTBEAT_INTERVAL)

@app.route("/")
def home():
    return "AtomicBot is running."

if __name__ == "__main__":
    threading.Thread(target=trade_loop, daemon=True).start()
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)

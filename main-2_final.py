
import requests
import time
import threading
from flask import Flask

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # ← SETT INN DIN WEBHOOK HER
TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT"]
FAKE_BALANCE = 1000  # USDT
TRADE_PERCENT = 0.05

def send_to_discord(message):
    data = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Feil ved sending til Discord: {e}")

def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        return float(response.json()["price"])
    except:
        return None

def simulate_trades():
    amount = FAKE_BALANCE * TRADE_PERCENT
    for symbol in TOKENS:
        price = get_price(symbol)
        if price:
            qty = amount / price
            print(f"Simulated BUY: {symbol} at {price} | Amount: ${amount:.2f} | Qty: {qty}")
            send_to_discord(f"💰 Simulated BUY: {symbol} at ${price:.2f} | Amount: ${amount:.2f} | Qty: {qty:.4f}")

def heartbeat_loop():
    count = 1
    while count <= 24:
        send_to_discord(f"⏰ Hourly report: {count}/24 completed.")
        count += 1
        time.sleep(3600)

def trading_loop():
    while True:
        simulate_trades()
        time.sleep(3600)

# Start både heartbeat og trading i bakgrunn
threading.Thread(target=heartbeat_loop, daemon=True).start()
threading.Thread(target=trading_loop, daemon=True).start()

@app.route("/")
def index():
    return "Atomicbot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

# main.py (eller atomicbot.py)
import time
import requests
import pytz
import datetime
from websocket import create_connection

# Placeholder-funksjon for "live_prices" via WebSocket

def live_prices():
    try:
        ws = create_connection("wss://stream.binance.com:9443/ws/!ticker_24hr@arr")
        data = ws.recv()
        ws.close()
        return data
    except Exception as e:
        print("WebSocket error:", e)
        return None

def simulate_trade(symbol, price, quantity):
    print(f"Simulated trade: {symbol} at ${price} for {quantity} units")

# Dummy strategy

def basic_strategy(prices):
    for asset in ["BTCUSDT", "ETHUSDT", "BNBUSDT"]:
        price = prices.get(asset)
        if price:
            simulate_trade(asset, price, 50 / float(price))

def run_bot():
    while True:
        print("Fetching live prices...")
        data = live_prices()
        if not data:
            time.sleep(10)
            continue

        # Dummy data decoding for now
        prices = {
            "BTCUSDT": "117000",
            "ETHUSDT": "2950",
            "BNBUSDT": "690"
        }

        basic_strategy(prices)

        print("Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    run_bot()

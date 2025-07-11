
import time
import threading
import requests
import csv
from flask import Flask, jsonify
from collections import defaultdict

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"
TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT"]
TRADE_INTERVAL = 60
HEARTBEAT_INTERVAL = 3600

trade_log = []
strategy_stats = defaultdict(lambda: {"count": 0, "volume": 0.0})

def strategy_basic(symbol, price):
    return True

def strategy_even_minute(symbol, price):
    return int(time.time() / 60) % 2 == 0

def strategy_expensive_only(symbol, price):
    return price > 500

def choose_strategy():
    sec = int(time.time())
    if sec % 1800 < 600:
        return strategy_basic, "basic"
    elif sec % 1800 < 1200:
        return strategy_even_minute, "even_minute"
    else:
        return strategy_expensive_only, "expensive_only"

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def send_to_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Failed to send message to Discord: {e}")

def log_trade_to_csv(entry):
    try:
        with open("trades.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([entry["timestamp"], entry["strategy"], entry["symbol"], entry["price"], entry["amount"], entry["qty"]])
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def simulate_trades():
    balance = 1000
    amount = balance * 0.05
    strategy_fn, strategy_name = choose_strategy()

    for symbol in TOKENS:
        price = get_price(symbol)
        if price and strategy_fn(symbol, price):
            qty = amount / price
            entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
                "price": price,
                "qty": qty,
                "amount": amount,
                "strategy": strategy_name
            }
            trade_log.append(entry)
            strategy_stats[strategy_name]["count"] += 1
            strategy_stats[strategy_name]["volume"] += amount
            log_trade_to_csv(entry)
            print(f"💰 BUY [{strategy_name}] {symbol} @ ${price:.2f} | ${amount:.2f} | Qty: {qty:.4f}")

def hourly_report():
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        total_trades = len(trade_log)
        total_volume = sum([x["amount"] for x in trade_log])

        message = f"📊 **Hourly Trading Summary**\n"
        message += f"🧾 Total trades: {total_trades}\n💸 Total simulated spend: ${total_volume:.2f}\n"

        for strat, stats in strategy_stats.items():
            message += f"🔁 Strategy '{strat}': {stats['count']} trades | Simulated spend: ${stats['volume']:.2f}\n"

        print(message)
        send_to_discord(message)
        trade_log.clear()
        strategy_stats.clear()

@app.route("/")
def home():
    return "✅ AtomicBot backend is alive and responding!"

@app.route("/api/trades")
def get_trades():
    return jsonify(trade_log)

def start_background_threads():
    print("🚀 Starting background threads...")
    threading.Thread(target=hourly_report, daemon=True).start()
    threading.Thread(target=lambda: (time.sleep(10), [simulate_trades() or time.sleep(TRADE_INTERVAL) for _ in iter(int, 1)]), daemon=True).start()

start_background_threads()

if __name__ == "__main__":
    print("✅ Flask app starting via __main__")
    app.run(host="0.0.0.0", port=8080)

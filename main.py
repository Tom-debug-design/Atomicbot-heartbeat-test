
import time
import threading
import requests
import csv
from flask import Flask, jsonify
from collections import defaultdict
import statistics

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"
TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
TRADE_INTERVAL = 60
HEARTBEAT_INTERVAL = 3600

trade_log = []
strategy_stats = defaultdict(lambda: {"count": 0, "volume": 0.0})
strategy_score = defaultdict(float)
last_best_strategy = "basic"

# === Strategy functions ===

def get_prices(symbol, limit=20):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit={limit}"
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        return [float(k[4]) for k in r.json()]  # close prices
    except:
        return []

def rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = [prices[i+1] - prices[i] for i in range(period)]
    gains = sum(d for d in deltas if d > 0)
    losses = -sum(d for d in deltas if d < 0)
    if losses == 0:
        return 100
    rs = gains / losses
    return 100 - (100 / (1 + rs))

def ma(prices, period):
    if len(prices) < period:
        return None
    return statistics.mean(prices[-period:])

def strategy_basic(symbol, price): return True
def strategy_even_minute(symbol, price): return int(time.time() / 60) % 2 == 0
def strategy_expensive_only(symbol, price): return price > 500

def strategy_ma(symbol, price):
    prices = get_prices(symbol)
    ma5 = ma(prices, 5)
    ma10 = ma(prices, 10)
    return ma5 and ma10 and ma5 > ma10

def strategy_rsi(symbol, price):
    prices = get_prices(symbol)
    val = rsi(prices)
    return val and val < 30

def strategy_combo(symbol, price):
    prices = get_prices(symbol)
    ma5 = ma(prices, 5)
    ma10 = ma(prices, 10)
    rsi_val = rsi(prices)
    return ma5 and ma10 and rsi_val and ma5 > ma10 and rsi_val < 30

STRATEGIES = {
    "basic": strategy_basic,
    "even_minute": strategy_even_minute,
    "expensive_only": strategy_expensive_only,
    "trend_ma": strategy_ma,
    "rsi_low": strategy_rsi,
    "trend_rsi_combo": strategy_combo
}

def choose_strategy():
    global last_best_strategy
    return STRATEGIES.get(last_best_strategy, strategy_basic), last_best_strategy

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        return float(r.json()["price"])
    except:
        return None

def send_to_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    except:
        pass

def log_trade_csv(entry):
    try:
        with open("trades.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([entry["timestamp"], entry["strategy"], entry["symbol"], entry["price"], entry["amount"], entry["qty"]])
    except:
        pass

def simulate_trades():
    global trade_log
    balance = 1000
    amount = balance * 0.05
    strat_fn, strat_name = choose_strategy()

    for symbol in TOKENS:
        price = get_price(symbol)
        if price and strat_fn(symbol, price):
            qty = amount / price
            entry = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "symbol": symbol,
                "price": price,
                "qty": qty,
                "amount": amount,
                "strategy": strat_name
            }
            trade_log.append(entry)
            strategy_stats[strat_name]["count"] += 1
            strategy_stats[strat_name]["volume"] += amount
            strategy_score[strat_name] += 1
            log_trade_csv(entry)
            print(f"💰 BUY [{strat_name}] {symbol} @ ${price:.2f} | ${amount:.2f} | Qty: {qty:.4f}")

def hourly_report():
    global trade_log, strategy_stats, strategy_score, last_best_strategy
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        total_trades = len(trade_log)
        total_volume = sum([x["amount"] for x in trade_log])
        msg = f"📊 **Hourly Trading Summary**\n🧾 Total trades: {total_trades}\n💸 Total simulated spend: ${total_volume:.2f}\n"
        for strat, stats in strategy_stats.items():
            msg += f"🔁 Strategy '{strat}': {stats['count']} trades | Spend: ${stats['volume']:.2f}\n"
        if strategy_score:
            best = max(strategy_score, key=strategy_score.get)
            last_best_strategy = best
            msg += f"🎯 Smart selector: Next hour = **{best}**"
        send_to_discord(msg)
        print(msg)
        trade_log.clear()
        strategy_stats.clear()
        strategy_score.clear()

@app.route("/")
def home():
    return "✅ TrendBot + RSI is running."

@app.route("/api/trades")
def get_trades():
    return jsonify(trade_log)

def start_threads():
    threading.Thread(target=hourly_report, daemon=True).start()
    threading.Thread(target=lambda: (time.sleep(5), [simulate_trades() or time.sleep(TRADE_INTERVAL) for _ in iter(int, 1)]), daemon=True).start()

start_threads()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

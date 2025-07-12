
import time
import threading
from flask import Flask, jsonify
from collections import defaultdict
import random

app = Flask(__name__)

TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
TRADE_INTERVAL = 60
EXIT_INTERVAL = 15
HEARTBEAT_INTERVAL = 3600

open_positions = {}
trade_history = []
strategy_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "pnl": 0.0, "count": 0})
last_strategy = "basic"

# --- SIMULERT BINANCE-API --- #
class FakeBinanceClient:
    def __init__(self):
        self.prices = {token: 100 + random.random() * 1000 for token in TOKENS}

    def get_price(self, symbol):
        base = self.prices[symbol]
        noise = random.uniform(-0.5, 0.5)
        new_price = round(base + noise, 2)
        self.prices[symbol] = new_price
        return new_price

    def order_market_buy(self, symbol, qty):
        return {
            "symbol": symbol,
            "side": "BUY",
            "status": "FILLED",
            "fills": [{"price": str(self.get_price(symbol))}]
        }

    def order_market_sell(self, symbol, qty):
        return {
            "symbol": symbol,
            "side": "SELL",
            "status": "FILLED",
            "fills": [{"price": str(self.get_price(symbol))}]
        }

client = FakeBinanceClient()

# --- Strategier --- #
def strategy_basic(symbol, price): return True
def strategy_even(symbol, price): return int(time.time() / 60) % 2 == 0
def strategy_expensive(symbol, price): return price > 500

STRATEGIES = {
    "basic": strategy_basic,
    "even": strategy_even,
    "expensive": strategy_expensive,
}

def choose_strategy():
    global last_strategy
    return STRATEGIES.get(last_strategy, strategy_basic), last_strategy

# --- Tradinglogikk --- #
def simulate_entry():
    strat_fn, strat_name = choose_strategy()
    amount = 50

    for token in TOKENS:
        if token in open_positions:
            continue

        price = client.get_price(token)
        if not price or not strat_fn(token, price):
            continue

        qty = amount / price
        order = client.order_market_buy(token, qty)
        entry_price = float(order["fills"][0]["price"])

        open_positions[token] = {
            "entry_price": entry_price,
            "qty": qty,
            "amount": amount,
            "strategy": strat_name,
            "time": time.strftime("%H:%M:%S")
        }

        print(f"📥 Simulated BUY [{strat_name}] {token} @ ${entry_price:.2f} | Qty: {qty:.4f}")

def check_exit():
    for token, pos in list(open_positions.items()):
        current_price = client.get_price(token)
        entry = pos["entry_price"]
        qty = pos["qty"]
        change = (current_price - entry) / entry

        if change >= 0.02 or change <= -0.01:
            side = "SELL"
            order = client.order_market_sell(token, qty)
            exit_price = float(order["fills"][0]["price"])
            pnl = (exit_price - entry) * qty
            strat = pos["strategy"]

            strategy_stats[strat]["count"] += 1
            strategy_stats[strat]["pnl"] += pnl
            if pnl >= 0:
                strategy_stats[strat]["wins"] += 1
            else:
                strategy_stats[strat]["losses"] += 1

            trade_history.append({
                "token": token,
                "strategy": strat,
                "pnl": pnl,
                "entry": entry,
                "exit": exit_price,
                "qty": qty,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            })

            print(f"✅ EXIT [{strat}] {token} | Entry: ${entry:.2f} → Exit: ${exit_price:.2f} | PnL: ${pnl:.2f}")
            del open_positions[token]

def hourly_report():
    global strategy_stats
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        report = f"📊 **Hourly Report**\n"
        total_pnl = sum(stat["pnl"] for stat in strategy_stats.values())
        report += f"💸 Total Simulated PnL: ${total_pnl:.2f}\n"
        for strat, stat in strategy_stats.items():
            report += f"🔁 '{strat}': {stat['count']} trades | PnL: ${stat['pnl']:.2f}\n"
        best = max(strategy_stats.items(), key=lambda x: x[1]["pnl"])[0]
        global last_strategy
        last_strategy = best
        report += f"🎯 Next strategy: **{best}**"
        print(report)
        strategy_stats.clear()

@app.route("/")
def home():
    return "✅ Simulated Binance Bot Active"

@app.route("/api/open")
def open_view():
    return jsonify(open_positions)

@app.route("/api/history")
def history_view():
    return jsonify(trade_history)

# Start tråder
threading.Thread(target=lambda: (time.sleep(5), [simulate_entry() or time.sleep(60) for _ in iter(int, 1)]), daemon=True).start()
threading.Thread(target=lambda: (time.sleep(10), [check_exit() or time.sleep(15) for _ in iter(int, 1)]), daemon=True).start()
threading.Thread(target=hourly_report, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


import time
import threading
import requests
from flask import Flask, jsonify
from collections import defaultdict

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"
TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
HEARTBEAT_INTERVAL = 3600

open_positions = {}
trade_history = []
strategy_stats = defaultdict(lambda: {"wins": 0, "losses": 0, "pnl": 0.0, "count": 0})
last_strategy = "basic"

def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        return float(r.json()["price"])
    except:
        return None

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

def simulate_entry():
    strat_fn, strat_name = choose_strategy()
    amount = 50

    for token in TOKENS:
        if token in open_positions:
            continue

        price = get_price(token)
        if not price or not strat_fn(token, price):
            continue

        qty = amount / price
        open_positions[token] = {
            "entry_price": price,
            "qty": qty,
            "amount": amount,
            "strategy": strat_name,
            "time": time.strftime("%H:%M:%S")
        }

        msg = f"📥 Entry [{strat_name}] {token} @ ${price:.2f} | Qty: {qty:.4f}"
        print(msg)
        send_to_discord(msg)

def check_exit():
    for token, pos in list(open_positions.items()):
        current_price = get_price(token)
        if not current_price:
            continue

        entry = pos["entry_price"]
        qty = pos["qty"]
        change = (current_price - entry) / entry

        exit_reason = None
        if change >= 0.02:
            exit_reason = "🎯 Take Profit"
        elif change <= -0.01:
            exit_reason = "🛑 Stop Loss"

        if exit_reason:
            pnl = (current_price - entry) * qty
            strat = pos["strategy"]
            strategy_stats[strat]["count"] += 1
            strategy_stats[strat]["pnl"] += pnl
            if pnl >= 0:
                strategy_stats[strat]["wins"] += 1
            else:
                strategy_stats[strat]["losses"] += 1

            msg = f"{exit_reason} [{strat}] {token} | Entry: ${entry:.2f} → Exit: ${current_price:.2f} | PnL: ${pnl:.2f}"
            print(msg)
            send_to_discord(msg)

            trade_history.append({
                "token": token,
                "strategy": strat,
                "pnl": pnl,
                "entry": entry,
                "exit": current_price,
                "qty": qty,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            })

            del open_positions[token]

def hourly_report():
    global strategy_stats
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        report = f"📊 **Hourly Trading Report**\n"
        total_pnl = sum(stat["pnl"] for stat in strategy_stats.values())
        report += f"💸 Total PnL: ${total_pnl:.2f}\n"
        for strat, stat in strategy_stats.items():
            report += f"🔁 '{strat}': {stat['count']} trades | Wins: {stat['wins']} | Losses: {stat['losses']} | PnL: ${stat['pnl']:.2f}\n"
        best = max(strategy_stats.items(), key=lambda x: x[1]["pnl"])[0]
        global last_strategy
        last_strategy = best
        report += f"🎯 Next strategy: **{best}**"
        send_to_discord(report)
        strategy_stats.clear()

def send_to_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except:
        pass

@app.route("/")
def home():
    return "✅ Bot Running: Fast exits, smart entries."

@app.route("/api/open")
def open_trades():
    return jsonify(open_positions)

@app.route("/api/history")
def history():
    return jsonify(trade_history)

# Entry every 60s
threading.Thread(target=lambda: (time.sleep(5), [simulate_entry() or time.sleep(60) for _ in iter(int, 1)]), daemon=True).start()

# Exit check every 15s
threading.Thread(target=lambda: (time.sleep(10), [check_exit() or time.sleep(15) for _ in iter(int, 1)]), daemon=True).start()

# Hourly strategy eval
threading.Thread(target=hourly_report, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

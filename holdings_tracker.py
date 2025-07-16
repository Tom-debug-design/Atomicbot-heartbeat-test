import json
import os
from datetime import datetime

HOLDINGS_FILE = "open_positions.json"

def load_holdings():
    if os.path.exists(HOLDINGS_FILE):
        with open(HOLDINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_holdings(holdings):
    with open(HOLDINGS_FILE, "w") as f:
        json.dump(holdings, f, indent=2)

def check_sell_conditions(symbol, current_price, rsi):
    holdings = load_holdings()
    if symbol not in holdings:
        return None

    entry = holdings[symbol]
    bought_price = entry["price"]
    time_bought = entry["time"]
    change_pct = ((current_price - bought_price) / bought_price) * 100

    if rsi > 70 or change_pct >= 3 or change_pct <= -2:
        del holdings[symbol]
        save_holdings(holdings)
        return f"💸 SELL {symbol} at ${current_price:.2f} | PnL: {change_pct:.2f}% | RSI: {rsi:.1f}"
    return None

def log_buy(symbol, price):
    holdings = load_holdings()
    holdings[symbol] = {"price": price, "time": datetime.utcnow().isoformat()}
    save_holdings(holdings)

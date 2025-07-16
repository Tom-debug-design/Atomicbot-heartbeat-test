import json
import os
from datetime import datetime

LOG_FILE = "trades_log.json"

def log_trade(trade):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": trade['symbol'],
        "price": trade['price'],
        "qty": trade['qty']
    }
    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    data.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

def report_pnl(daily=False):
    if not os.path.exists(LOG_FILE):
        return
    with open(LOG_FILE, "r") as f:
        trades = json.load(f)

    total = 0
    count = 0
    for trade in trades:
        if daily:
            if datetime.fromisoformat(trade['timestamp']).date() != datetime.utcnow().date():
                continue
        total += trade['price'] * trade['qty']
        count += 1
    avg = total / count if count else 0
    print(f"PnL Report {'(Daily)' if daily else ''}: {count} trades, Total Volume: ${total:,.2f}, Avg per trade: ${avg:,.2f}")

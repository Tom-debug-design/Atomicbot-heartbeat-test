import json
import os
from datetime import datetime

LOG_FILE = "trade_log.json"

def log_trade(trade_data):
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                log = json.load(f)
        else:
            log = []

        log.append(trade_data)

        with open(LOG_FILE, "w") as f:
            json.dump(log, f, indent=2)
    except Exception as e:
        print(f"[log_trade error] {e}")

def report_pnl(daily=False):
    try:
        if not os.path.exists(LOG_FILE):
            return

        with open(LOG_FILE, "r") as f:
            trades = json.load(f)

        now = datetime.utcnow()
        filtered = []

        for trade in trades:
            trade_time = datetime.strptime(trade["timestamp"], "%Y-%m-%d %H:%M:%S")
            if daily:
                if trade_time.date() == now.date():
                    filtered.append(trade)
            else:
                if now.hour == trade_time.hour and now.date() == trade_time.date():
                    filtered.append(trade)

        total_buys = sum(t["amount"] for t in filtered if t["side"] == "buy")
        total_sells = sum(t["amount"] for t in filtered if t["side"] == "sell")
        trades_count = len(filtered)

        pnl = total_sells - total_buys
        report = f"""
📊 {'Daily' if daily else 'Hourly'} PnL Report:
Total Trades: {trades_count}
Total Buys: ${total_buys:.2f}
Total Sells: ${total_sells:.2f}
PnL: ${pnl:.2f}
"""
        from discord_logger import send_discord_message
        send_discord_message(report.strip())

    except Exception as e:
        print(f"[report_pnl error] {e}")

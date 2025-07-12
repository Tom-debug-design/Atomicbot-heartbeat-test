# AtomicBot Enhanced Reporting & Learning Dispatch
import time
import threading
import requests
import random
from collections import defaultdict
from datetime import datetime, timedelta

# Discord webhook for logs
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_here"

TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
STRATEGIES = ["basic", "even_minute", "expensive_only", "aggressive_v1"]
HEARTBEAT_INTERVAL = 3600
DAILY_REPORT_HOUR_UTC = 6

trade_log = []
strategy_stats = defaultdict(lambda: {"count": 0, "wins": 0, "losses": 0, "pnl": 0.0})

def get_price(symbol):
    return round(100 + random.uniform(-1, 1), 2)

def send_to_discord(message):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Discord send failed:", e)

# Simulated buy/sell with outcome

def simulate_trade():
    for symbol in TOKENS:
        price = get_price(symbol)
        strategy = random.choice(STRATEGIES)
        qty = round(50 / price, 4)
        exit_price = price * (1 + random.uniform(-0.02, 0.025))
        pnl = (exit_price - price) * qty

        trade = {
            "timestamp": datetime.utcnow(),
            "symbol": symbol,
            "strategy": strategy,
            "entry": price,
            "exit": exit_price,
            "qty": qty,
            "pnl": pnl
        }
        trade_log.append(trade)

        strategy_stats[strategy]["count"] += 1
        strategy_stats[strategy]["pnl"] += pnl
        if pnl >= 0:
            strategy_stats[strategy]["wins"] += 1
        else:
            strategy_stats[strategy]["losses"] += 1

        print(f"[TRADE] {strategy} {symbol} @ ${price:.2f} → ${exit_price:.2f} | PnL: ${pnl:.2f}")

# Hourly PnL summary

def hourly_report():
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        last_hour_trades = [t for t in trade_log if t["timestamp"] > one_hour_ago]

        report = f"🕐 **Hourly Report ({now.strftime('%H:%M UTC')})**\n"
        total_pnl = sum(t["pnl"] for t in last_hour_trades)
        report += f"💸 Total PnL: ${total_pnl:.2f}\n"

        strat_pnl = defaultdict(float)
        for t in last_hour_trades:
            strat_pnl[t["strategy"]] += t["pnl"]

        for strat in STRATEGIES:
            pnl = strat_pnl[strat]
            count = len([t for t in last_hour_trades if t["strategy"] == strat])
            report += f"🔹 `{strat}`: {count} trades | PnL: ${pnl:.2f}\n"

        send_to_discord(report)

# Daily summary at 06:00 UTC

def daily_report():
    while True:
        now = datetime.utcnow()
        next_6utc = now.replace(hour=DAILY_REPORT_HOUR_UTC, minute=0, second=0, microsecond=0)
        if now >= next_6utc:
            next_6utc += timedelta(days=1)
        time.sleep((next_6utc - now).total_seconds())

        since = datetime.utcnow() - timedelta(hours=24)
        last_day = [t for t in trade_log if t["timestamp"] > since]

        report = f"📅 **Daily Report (06:00 UTC)**\n"
        total_pnl = sum(t["pnl"] for t in last_day)
        report += f"💰 Total 24h PnL: ${total_pnl:.2f}\n"

        for strat in STRATEGIES:
            trades = [t for t in last_day if t["strategy"] == strat]
            pnl = sum(t["pnl"] for t in trades)
            wins = len([t for t in trades if t["pnl"] > 0])
            losses = len(trades) - wins
            report += f"🔸 `{strat}`: {len(trades)} trades | ✅ {wins} | ❌ {losses} | PnL: ${pnl:.2f}\n"

        send_to_discord(report)

# Run

def start_bot():
    threading.Thread(target=hourly_report, daemon=True).start()
    threading.Thread(target=daily_report, daemon=True).start()
    while True:
        simulate_trade()
        time.sleep(5)

if __name__ == "__main__":
    start_bot()

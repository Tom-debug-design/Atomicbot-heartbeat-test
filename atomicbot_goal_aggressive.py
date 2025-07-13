import time
import threading
import requests
import random
from datetime import datetime, timedelta, timezone
from collections import defaultdict

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_here"

TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
STRATEGIES = ["basic", "even_minute", "expensive_only", "aggressive_v2", "gap_and_go"]
GOAL_START = 50.0
daily_goal = GOAL_START
current_day = None
trade_log = []

def get_price(symbol):
    return round(100 + random.uniform(-1, 1), 2)

def send_to_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("Discord error:", e)

def simulate_trade():
    for symbol in TOKENS:
        strategy = random.choice(STRATEGIES)
        price = get_price(symbol)
        qty = round(50 / price, 4)
        exit_price = price * (1 + random.uniform(-0.02, 0.025))
        pnl = (exit_price - price) * qty

        trade = {
            "timestamp": datetime.now(timezone.utc),
            "symbol": symbol,
            "strategy": strategy,
            "entry": price,
            "exit": exit_price,
            "qty": qty,
            "pnl": pnl
        }
        trade_log.append(trade)
        print(f"📈 [{strategy}] {symbol} ${price:.2f} → ${exit_price:.2f} | PnL: ${pnl:.2f}")

def hourly_report():
    while True:
        time.sleep(3600)
        now = datetime.now(timezone.utc)
        one_hour_ago = now - timedelta(hours=1)
        recent = [t for t in trade_log if t["timestamp"] > one_hour_ago]
        if not recent:
            print(f"⏰ No trades to report for {now.strftime('%H:%M')} UTC")
            continue
        msg = f"🕐 **Hourly Report ({now.strftime('%H:%M UTC')})**\n"
        total_pnl = sum(t["pnl"] for t in recent)
        msg += f"💰 Total PnL: ${total_pnl:.2f}\n"
        for s in STRATEGIES:
            strat_trades = [t for t in recent if t["strategy"] == s]
            strat_pnl = sum(t["pnl"] for t in strat_trades)
            msg += f"🔹 `{s}`: {len(strat_trades)} trades | PnL: ${strat_pnl:.2f}\n"
        send_to_discord(msg)

def daily_report():
    global daily_goal, current_day
    while True:
        now = datetime.now(timezone.utc)
        if current_day != now.date() and now.hour == 6:
            last_24h = [t for t in trade_log if t["timestamp"] > now - timedelta(hours=24)]
            total_pnl = sum(t["pnl"] for t in last_24h)

            report = f"📅 **Daily Report (06:00 UTC)**\n🎯 Goal: ${daily_goal:.2f} | Result: ${total_pnl:.2f}\n"
            if total_pnl >= daily_goal:
                daily_goal += 10
                report += f"✅ Goal reached! New goal: ${daily_goal:.2f}\n"
            else:
                report += f"❌ Goal not reached. Try again tomorrow.\n"

            for s in STRATEGIES:
                trades = [t for t in last_24h if t["strategy"] == s]
                pnl = sum(t["pnl"] for t in trades)
                wins = len([t for t in trades if t["pnl"] > 0])
                losses = len(trades) - wins
                report += f"🔸 `{s}`: {len(trades)} trades | ✅ {wins} | ❌ {losses} | PnL: ${pnl:.2f}\n"

            send_to_discord(report)
            current_day = now.date()
        time.sleep(60)

def run_bot():
    threading.Thread(target=hourly_report, daemon=True).start()
    threading.Thread(target=daily_report, daemon=True).start()
    while True:
        simulate_trade()
        time.sleep(5)

if __name__ == "__main__":
    run_bot()
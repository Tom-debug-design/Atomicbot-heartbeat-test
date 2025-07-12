import time
import threading
import requests
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_here"
TOKENS = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
STRATEGIES = ["basic", "even_minute", "expensive_only", "aggressive_v1"]

trade_log = []
daily_goal = 50.0
current_day = None

def get_price(symbol):
    return round(100 + random.uniform(-1, 1), 2)

def send_to_discord(msg):
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("❌ Discord error:", e)

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
        print(f"📈 {strategy} {symbol} ${price:.2f} → ${exit_price:.2f} | PnL: ${pnl:.2f}")

def hourly_summary():
    while True:
        now = datetime.now(timezone.utc)
        last_hour = now - timedelta(hours=1)
        recent = [t for t in trade_log if t["timestamp"] > last_hour]
        if not recent:
            print(f"⏰ No trades to report for {now.strftime('%H:%M')} UTC")
        else:
            msg = f"🕐 **Hourly Report ({now.strftime('%H:%M UTC')})**\n"
            total_pnl = sum(t["pnl"] for t in recent)
            msg += f"💰 PnL: ${total_pnl:.2f}\n"
            for strat in STRATEGIES:
                trades = [t for t in recent if t["strategy"] == strat]
                pnl = sum(t["pnl"] for t in trades)
                msg += f"🔹 `{strat}`: {len(trades)} trades | PnL: ${pnl:.2f}\n"
            send_to_discord(msg)
        time.sleep(3600)

def daily_summary():
    global daily_goal, current_day
    while True:
        now = datetime.now(timezone.utc)
        if current_day != now.date() and now.hour == 6:
            last_24h = [t for t in trade_log if t["timestamp"] > now - timedelta(hours=24)]
            total_pnl = sum(t["pnl"] for t in last_24h)

            report = f"📅 **Daily Report (06:00 UTC)**\n🎯 Goal: ${daily_goal:.2f} | Result: ${total_pnl:.2f}\n"
            if total_pnl >= daily_goal:
                report += f"✅ Goal reached! Setting new goal: ${daily_goal + 10:.2f}\n"
                daily_goal += 10
            else:
                report += f"❌ Goal not reached. Trying again tomorrow.\n"

            for strat in STRATEGIES:
                strat_trades = [t for t in last_24h if t["strategy"] == strat]
                strat_pnl = sum(t["pnl"] for t in strat_trades)
                wins = len([t for t in strat_trades if t["pnl"] > 0])
                losses = len(strat_trades) - wins
                report += f"🔸 `{strat}`: {len(strat_trades)} trades | ✅ {wins} | ❌ {losses} | PnL: ${strat_pnl:.2f}\n"

            send_to_discord(report)
            current_day = now.date()
        time.sleep(60)

def run_bot():
    threading.Thread(target=hourly_summary, daemon=True).start()
    threading.Thread(target=daily_summary, daemon=True).start()
    while True:
        simulate_trade()
        time.sleep(5)

if __name__ == "__main__":
    run_bot()
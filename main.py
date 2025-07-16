import os
import threading
import time
import datetime
from flask import Flask
from discord_logger import send_discord_message
from strategy import generate_trades
from pnl_tracker import log_trade, report_pnl

app = Flask(__name__)

def bot_loop():
    while True:
        now = datetime.datetime.utcnow()
        try:
            if now.minute == 0:
                send_discord_message(f"🕒 Hourly status: AtomicBot v3 running ({now})")
                report_pnl()
            if now.hour == 6 and now.minute == 0:
                send_discord_message(f"📅 Daily Report @ {now.strftime('%H:%M')} UTC")
                report_pnl(daily=True)

            trades = generate_trades()
            for trade in trades:
                send_discord_message(trade['message'])
                log_trade(trade)
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(15)

@app.route("/")
def index():
    return "AtomicBot Aggressive v3 is running."

if __name__ == "__main__":
    t = threading.Thread(target=bot_loop)
    t.daemon = True
    t.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

import os
import threading
import time
import datetime
from flask import Flask
from discord_logger import send_discord_message
from strategies import check_buy_signal
from pnl_tracker import log_trade, report_pnl

app = Flask(__name__)

@app.route("/")
def home():
    return "AtomicBot v3 is alive!"

def bot_loop():
    while True:
        now = datetime.datetime.utcnow()
        try:
            if now.minute == 0:
                send_discord_message(f"🕐 Hourly status: AtomicBot is online ({now})")
                report_pnl()
            if now.hour == 6 and now.minute == 0:
                send_discord_message(f"📊 Daily Report @ {now.strftime('%H:%M')} UTC")
                report_pnl(daily=True)
        except Exception as e:
            print("Loop error:", e)
        time.sleep(15)

if __name__ == "__main__":
    threading.Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

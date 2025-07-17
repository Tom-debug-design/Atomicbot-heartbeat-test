from flask import Flask
import threading
import schedule
import time
from discord_logger import send_discord_message
from pnl_tracker import report_pnl
from trading import perform_trading_loop

app = Flask(__name__)

@app.route('/')
def home():
    return "AtomicBot v3.4 is alive"

def scheduler_loop():
    schedule.every().hour.at(":00").do(lambda: send_discord_message("🔁 Hourly status: AtomicBot is online"))
    schedule.every().hour.at(":01").do(lambda: report_pnl(hourly=True))
    schedule.every().day.at("06:00").do(lambda: report_pnl(daily=True))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=scheduler_loop).start()
    perform_trading_loop()
    app.run(host="0.0.0.0", port=8080)


from flask import Flask
from heartbeat import send_heartbeat
from discord_logger import send_discord_message
from pnl_tracker import log_trade, report_pnl
from trading import perform_trading_loop
import schedule
import time
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "AtomicBot v3.1 is running"

def run_schedule():
    schedule.every().hour.at(":00").do(lambda: send_discord_message("🔁 Hourly status: AtomicBot is online"))
    schedule.every().hour.at(":01").do(lambda: report_pnl(hourly=True))
    schedule.every().day.at("06:00").do(lambda: report_pnl(daily=True))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=run_schedule).start()
    perform_trading_loop()
    app.run(host='0.0.0.0', port=8080)

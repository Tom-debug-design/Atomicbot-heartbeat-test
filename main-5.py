from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from discord_logger import send_discord_message
from pnl_tracker import log_trade, report_pnl
from learner import get_best_tokens, get_best_strategy
from strategy import check_buy_signal
import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "AtomicBot v3 AI-PNL Loop is running"

def run_bot():
    now = datetime.datetime.utcnow()
    tokens = get_best_tokens(top_n=5)
    strategy = get_best_strategy()
    for token in tokens:
        if check_buy_signal(token, strategy):
            price = round(random.uniform(0.3, 3000), 2)
            qty = round(50 / price, 6)
            pnl = round(random.uniform(-2, 5), 2)
            rsi = random.randint(20, 80)
            trade = {
                "symbol": token,
                "price": price,
                "qty": qty,
                "strategy": strategy,
                "rsi": rsi,
                "pnl": pnl
            }
            log_trade(trade)
            send_discord_message(f"BUY {token} using {strategy} | PnL: {pnl:.2f}%")

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_bot, 'interval', seconds=15)
    scheduler.add_job(lambda: report_pnl(daily=False), 'cron', minute=0)
    scheduler.start()
    app.run(host='0.0.0.0', port=8000)

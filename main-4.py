import os
import threading
import time
import datetime
from flask import Flask
from discord_logger import send_discord_message
from learner import get_best_tokens, get_best_strategy
from strategy import check_buy_signal
from pnl_tracker import log_trade, report_pnl

app = Flask(__name__)

@app.route("/")
def home():
    return "AtomicBot v3 AI Loop is running!"

def bot_loop():
    while True:
        now = datetime.datetime.utcnow()
        try:
            if now.minute == 0:
                send_discord_message(f"🔵 Hourly status: AtomicBot AI Loop running ({now})")
                report_pnl()

            if now.hour == 6 and now.minute == 0:
                send_discord_message(f"📘 Daily Report @ {now.strftime('%H:%M')} UTC")
                report_pnl(daily=True)

            best_tokens = get_best_tokens(top_n=5)
            strategy = get_best_strategy()

            for token in best_tokens:
                if check_buy_signal(token, strategy):
                    price = 30000  # placeholder for current price
                    qty = 0.001     # placeholder qty
                    send_discord_message(f"🚀 BUY: {token} using {strategy} strategy | Price: ${price} | Qty: {qty}")
                    log_trade({"symbol": token, "price": price, "qty": qty, "strategy": strategy, "timestamp": str(now)})

        except Exception as e:
            send_discord_message(f"⚠️ Bot error: {e}")

        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=bot_loop).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
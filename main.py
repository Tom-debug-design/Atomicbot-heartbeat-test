import os
import threading
import time
from flask import Flask
from discord_logger import send_discord_message
from trade_simulator import simulate_trades

app = Flask(__name__)

def heartbeat_loop():
    while True:
        try:
            send_discord_message("💓 Heartbeat: AtomicBot is alive and kicking!")
            simulate_trades()
        except Exception as e:
            print(f"Failed in loop: {e}")
        time.sleep(60)

@app.route("/")
def index():
    return "AtomicBot is running"

if __name__ == "__main__":
    t = threading.Thread(target=heartbeat_loop)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

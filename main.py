import os
import threading
import time
from flask import Flask
from discord_logger import send_discord_message

app = Flask(__name__)

# Funksjon som sender heartbeat hvert minutt
def heartbeat_loop():
    while True:
        try:
            send_discord_message("💓 Heartbeat: AtomicBot is alive and kicking!")
        except Exception as e:
            print(f"Failed to send Discord message: {e}")
        time.sleep(60)

# Flask-rute bare for testing / ping
@app.route("/")
def index():
    return "AtomicBot is running"

if __name__ == "__main__":
    # Start heartbeat i bakgrunnen
    t = threading.Thread(target=heartbeat_loop)
    t.daemon = True
    t.start()

    # Start Flask-server (nødvendig for Railway!)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

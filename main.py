from flask import Flask
import requests
from threading import Thread
import time
import pytz
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
TIMEZONE = pytz.timezone("Europe/Oslo")

def send_heartbeat(message):
    if WEBHOOK_URL:
        requests.post(WEBHOOK_URL, json={"content": message})

def hourly_report():
    for _ in range(24):
        send_heartbeat("⏱️ Hourly heartbeat check.")
        time.sleep(3600)
    daily_report()

def daily_report():
    while True:
        now = datetime.now(TIMEZONE)
        if now.hour == 6 and now.minute == 0:
            send_heartbeat("🌅 Daily heartbeat check at 06:00.")
            time.sleep(60)
        time.sleep(30)

@app.route("/")
def home():
    send_heartbeat("✅ Bot started and is alive!")
    Thread(target=hourly_report).start()
    return "✅ Bot started and is alive!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

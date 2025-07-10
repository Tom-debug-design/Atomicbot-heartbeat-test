import os
import requests
from flask import Flask
from threading import Thread
import time

app = Flask(__name__)

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def send_discord_message(content):
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json={"content": content})
        except Exception as e:
            print(f"Failed to send message: {e}")
    else:
        print("Webhook URL is not set.")

@app.route("/")
def home():
    return "Bot is alive!"

def schedule_reports():
    while True:
        current_hour = time.localtime().tm_hour
        current_minute = time.localtime().tm_min

        # Send rapport hver time det første døgnet (etter oppstart)
        if uptime_seconds < 86400 or (current_hour == 6 and current_minute == 0):
            send_discord_message("📡 Heartbeat: Bot is running.")
        time.sleep(60)

# Start rapporterings-tråden
uptime_seconds = 0

def uptime_tracker():
    global uptime_seconds
    while True:
        time.sleep(1)
        uptime_seconds += 1

if __name__ == "__main__":
    Thread(target=schedule_reports, daemon=True).start()
    Thread(target=uptime_tracker, daemon=True).start()
    app.run(host="0.0.0.0", port=3000)

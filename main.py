import os
import time
import requests
from flask import Flask
from threading import Thread
from datetime import datetime, timedelta

app = Flask(__name__)
WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"

def send_discord_message(message):
    requests.post(WEBHOOK_URL, json={"content": message})

@app.route("/")
def home():
    return "Bot is alive!"

def schedule_reports():
    # Send ping on startup
    send_discord_message("✅ Bot has started and is alive!")

    # Report every hour for 24 hours
    for hour in range(24):
        time.sleep(3600)
        send_discord_message(f"⏰ Hourly report: {hour + 1}/24 completed.")

    # Daily report at 06:00
    while True:
        now = datetime.now()
        next_report = now.replace(hour=6, minute=0, second=0, microsecond=0)
        if next_report <= now:
            next_report += timedelta(days=1)
        time_to_wait = (next_report - now).total_seconds()
        time.sleep(time_to_wait)
        send_discord_message("📅 Daily report: Bot is alive and running.")

def run_scheduler():
    thread = Thread(target=schedule_reports)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    run_scheduler()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

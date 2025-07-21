
import time
from datetime import datetime
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"

def send_to_discord(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("❌ Webhook-feil:", e)

def send_hourly_report():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    send_to_discord(f"🕒 [Hourly Report] AtomicBot status OK at {now} UTC")

def send_daily_report():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    send_to_discord(f"📊 [Daily Report] (Mock) PnL: +$12.44 | Win-rate: 71% | Time: {now} UTC")

def start_reporting_loop():
    hour_count = 0
    while True:
        now = datetime.utcnow()
        if now.hour == 6 and now.minute == 0:
            send_daily_report()
            time.sleep(60)
        if hour_count >= 60:
            send_hourly_report()
            hour_count = 0
        time.sleep(60)
        hour_count += 1

# Start
send_to_discord("📡 reporting_agent.py startet og overvåker rapportering.")
start_reporting_loop()

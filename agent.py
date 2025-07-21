import time
import requests
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQiikhyuPRJmjhqtESMhAlu3LxDfUrVgowxzSGyscEtiN"

def send_heartbeat():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = {
        "content": f"💓 Heartbeat: AtomicBot is alive at {now} UTC"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print(f"✅ Heartbeat sent at {now}")
        else:
            print(f"❌ Failed to send heartbeat: {response.status_code} {response.text}")
    except Exception as e:
        print(f"🔥 Exception during heartbeat: {e}")

def send_hourly_report():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = {
        "content": f"🕒 Hourly report: AtomicBot is still alive at {now} UTC"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print(f"✅ Hourly report sent at {now}")
        else:
            print(f"❌ Failed to send hourly report: {response.status_code} {response.text}")
    except Exception as e:
        print(f"🔥 Exception during hourly report: {e}")

if __name__ == "__main__":
    hour_last_sent = None
    while True:
        send_heartbeat()
        now = datetime.utcnow()
        if now.minute == 0 and hour_last_sent != now.hour:
            send_hourly_report()
            hour_last_sent = now.hour
        time.sleep(60)


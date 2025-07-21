import time
import requests
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"


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

if __name__ == "__main__":
    while True:
        send_heartbeat()
        time.sleep(60)

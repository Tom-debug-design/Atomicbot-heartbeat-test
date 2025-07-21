import requests
import time
from datetime import datetime

# ✅ Bruker riktig og fungerende webhook fra brukeren
WEBHOOK_URL = "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN"

def send_to_discord(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
    except Exception as e:
        print("Webhook-feil:", e)

def send_heartbeat():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    message = {
        "content": f"❤️ Heartbeat: AtomicBot is alive at {now} UTC"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print(f"✅ Heartbeat sent at {now}")
        else:
            print("❌ Webhook error:", response.status_code)
    except Exception as e:
        print("❌ Failed to send heartbeat:", e)

# ✅ Startmelding
send_to_discord("🟢 agent-3.py er LIVE og webhook fungerer ✅")

# Loop
while True:
    send_heartbeat()
    time.sleep(60)


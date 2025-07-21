
import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1391856933071560736/uh6LYuqM6uHLet9KhsgCS89FQiikhyuPRJmjhqtESMhA1u3LxDfUrVgowzzS9ryceEtkl"

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

# ✅ Testmelding rett etter oppstart
send_to_discord("🟢 agent.py is LIVE – webhook fungerer ✅")

# Start loop
while True:
    send_heartbeat()
    time.sleep(60)

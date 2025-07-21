import time
import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/your_webhook_here")

def log_heartbeat():
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    message = f"✅ Heartbeat: AtomicBot agent running at {timestamp}"
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        print("✅ Heartbeat sent to Discord")
    except Exception as e:
        print(f"❌ Failed to send heartbeat: {e}")

if __name__ == "__main__":
    while True:
        log_heartbeat()
        time.sleep(60)
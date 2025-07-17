import requests
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")  # Du kan også hardkode url her hvis du vil

def send_to_discord(message):
    if not WEBHOOK_URL:
        print(f"[Discord-fallback] {message}")
        return

    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"[Discord Error] {e}")


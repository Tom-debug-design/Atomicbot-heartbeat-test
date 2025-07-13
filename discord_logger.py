# discord_logger.py

import requests
from config import DISCORD_WEBHOOK_URL

def send_to_discord(message: str):
    try:
        data = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"[Discord ERROR] Status: {response.status_code} | Message: {response.text}")
    except Exception as e:
        print(f"[Discord EXCEPTION] {e}")

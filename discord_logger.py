import os
import requests

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_message(content):
    if DISCORD_WEBHOOK_URL:
        data = {"content": content}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            raise Exception(f"Discord webhook failed: {response.status_code} - {response.text}")
    else:
        raise Exception("DISCORD_WEBHOOK_URL is not set.")

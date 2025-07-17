import os
import requests

def send_discord_message(content):
    url = os.getenv("DISCORD_WEBHOOK_URL")
    if url:
        try:
            requests.post(url, json={"content": content})
        except Exception as e:
            print("[Discord error]", e)

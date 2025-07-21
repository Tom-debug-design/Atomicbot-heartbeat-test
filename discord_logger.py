
import requests
from config import DISCORD_WEBHOOK_URL

def send_to_discord(message):
    data = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Feil ved sending til Discord: {e}")

from flask import Flask
import os
import requests
from datetime import datetime

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_message(message):
    if DISCORD_WEBHOOK_URL:
        try:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        except Exception as e:
            print(f"Discord error: {e}")

@app.route("/")
def index():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"✅ Bot is alive at {now} UTC"
    send_discord_message(msg)
    return msg
from flask import Flask, request
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fqikhyuPRJmjhqmtESMhAlu3LxDfUrVggwxzSGyscEtiN")

@app.route("/")
def home():
    return "✅ Atomicbot webhook-app kjører!"

@app.route("/webhook")
def webhook():
    msg = request.args.get("msg", "👋 Standardmelding fra Railway webhook.")
    data = {
        "content": msg,
        "username": "Atomicbot Webhook"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK, json=data)
        return f"Status: {response.status_code}", response.status_code
    except Exception as e:
        return f"Feil: {e}", 500
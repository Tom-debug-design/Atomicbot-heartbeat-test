from flask import Flask, request
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1391855933071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJmjhqmtESMHaLu3LxDfUrVggwxzSGyscEtiN")

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
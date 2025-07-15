import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if not WEBHOOK_URL:
        return jsonify({"error": "DISCORD_WEBHOOK not set"}), 500
    msg = request.args.get("msg") or request.form.get("msg")
    if not msg:
        return jsonify({"error": "No msg parameter"}), 400
    data = {
        "content": msg,
        "username": "Atomicbot Webhook"
    }
    try:
        resp = requests.post(WEBHOOK_URL, json=data, timeout=10)
        return jsonify({"status_code": resp.status_code}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    status = "OK" if WEBHOOK_URL else "DISCORD_WEBHOOK not set"
    return f"Atomicbot relay status: {status}"

@app.route("/ping")
def ping():
    return "pong", 200

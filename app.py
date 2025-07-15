import os
import requests
from flask import Flask, request, jsonify
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if not WEBHOOK_URL:
        app.logger.error("Miljøvariabel DISCORD_WEBHOOK mangler!")
        return jsonify({"error": "DISCORD_WEBHOOK env var not set"}), 500
    msg = request.args.get("msg") or request.form.get("msg")
    if not msg:
        return jsonify({"error": "No msg parameter"}), 400
    data = {
        "content": msg,
        "username": "Atomicbot Webhook"
    }
    try:
        resp = requests.post(WEBHOOK_URL, json=data, timeout=10)
        app.logger.info(f"Respons fra Discord: {resp.status_code} {resp.text}")
        return jsonify({
            "status_code": resp.status_code,
            "discord_response": resp.text
        }), resp.status_code
    except Exception as e:
        app.logger.exception("Webhook send feilet:")
        return jsonify({"error": f"Exception: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def index():
    status = "OK" if WEBHOOK_URL else "DISCORD_WEBHOOK ikke satt!"
    return f"Atomicbot webhook relay er aktiv! Status: {status}"



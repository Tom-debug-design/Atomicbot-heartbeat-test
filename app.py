from flask import Flask
from discord_logger import send_discord_message

app = Flask(__name__)

@app.route("/")
def index():
    return "AtomicBot is running."

@app.route("/heartbeat")
def heartbeat():
    try:
        send_discord_message("💓 Heartbeat: AtomicBot is alive and kicking!")
        return "Heartbeat sent!"
    except Exception as e:
        return f"Discord error: {e}"

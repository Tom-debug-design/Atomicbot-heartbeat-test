from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Flask up!"

@app.route("/heartbeat")
def heartbeat():
    try:
        send_discord_message("💓 Heartbeat: AtomicBot is alive and kicking!")
        return "Heartbeat sent!"
    except Exception as e:
        print("🚨 Heartbeat-feil:", e)
        return f"Discord error: {str(e)}"


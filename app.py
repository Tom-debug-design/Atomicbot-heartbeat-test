# app.py

from flask import Flask
from heartbeat import send_heartbeat

app = Flask(__name__)

@app.route("/")
def home():
    return "AtomicBot is running!"

@app.route("/heartbeat")
def heartbeat():
    send_heartbeat()
    return "✅ Heartbeat sent to Discord!"

if __name__ == "__main__":
    app.run(debug=True)

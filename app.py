from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "✅ Flask up!"

@app.route("/heartbeat")
def heartbeat():
    return "✅ Heartbeat test OK!"

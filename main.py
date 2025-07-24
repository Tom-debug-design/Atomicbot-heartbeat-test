import random
import time
import datetime
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # <-- Sett inn din URL

def send_discord_message(message):
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print("Failed to send Discord message:", e)

def simulate_trade():
    action = random.choice(["BUY", "SELL"])
    pnl = round(random.uniform(-10, 10), 2)
    return action, pnl

def run_bot():
    while True:
        action, pnl = simulate_trade()
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        icon = "🔵" if action == "BUY" else "🔴"
        pnl_icon = "🟢" if pnl >= 0 else "🔴"
        message = f"{icon} {action} at {now} UTC | PnL: {pnl_icon} {pnl} USD"
        send_discord_message(message)
        time.sleep(60)
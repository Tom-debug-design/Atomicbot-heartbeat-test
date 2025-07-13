# heartbeat.py

from datetime import datetime
from discord_logger import send_to_discord

def send_heartbeat():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"✅ AtomicBot is alive – {now}"
    send_to_discord(message)

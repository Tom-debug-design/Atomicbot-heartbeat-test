
from discord_logger import send_to_discord
import time

# ✅ Testmelding ved oppstart
send_to_discord("🟢 agent.py is LIVE – webhook fungerer ✅")

def main_loop():
    while True:
        send_to_discord("❤️‍🔥 Heartbeat: AtomicBot is alive at " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        time.sleep(60)

if __name__ == "__main__":
    main_loop()

import time
from discord_logger import send_discord_message

if __name__ == "__main__":
    while True:
        try:
            send_discord_message("💓 Heartbeat: AtomicBot is alive and kicking!")
        except Exception as e:
            print(f"Failed to send Discord message: {e}")
        time.sleep(60)
from datetime import datetime
from discord_logger import send_to_discord

def report_pnl(mode="hourly"):
    now = datetime.utcnow()
    
    if mode == "daily":
        msg = f"📈 Daily Report generated at {now}"
    elif mode == "hourly":
        msg = f"📊 Hourly Report generated at {now}"
    else:
        msg = f"📎 General PnL Report at {now}"
    
    print(msg)
    send_to_discord(msg)


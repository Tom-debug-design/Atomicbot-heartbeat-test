
import threading
import time
from discord_logger import send_to_discord

# ✅ Testping ved oppstart
send_to_discord("🟢 Bot has started and webhook is ACTIVE ✅")

def heartbeat_loop():
    count = 1
    while count <= 24:
        send_to_discord(f"⏰ Hourly report: {count}/24 completed.")
        count += 1
        time.sleep(3600)

def trading_loop():
    # Simulert trading-loop
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT', 'AVAXUSDT', 'MATICUSDT']
    amount = 50.0  # 5% av 1000 USD
    for symbol in symbols:
        price = 100.0  # Simulert pris (erstatt med API-kall)
        qty = amount / price
        send_to_discord(
            f"💰 Simulated BUY: {symbol} at ${price:.2f} | Amount: ${amount:.2f} | Qty: {qty:.4f}"
        )
        time.sleep(10)  # Kort pause mellom handler

# Start trådene
threading.Thread(target=heartbeat_loop, daemon=True).start()
threading.Thread(target=trading_loop, daemon=True).start()

# Hold hovedtråden kjørende
while True:
    time.sleep(60)

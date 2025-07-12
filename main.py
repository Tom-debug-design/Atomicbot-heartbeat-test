import threading, time
from strategies import select_strategy
from client import FakeBinanceClient, live_prices
from scheduler import start_scheduler
from trader import run_trading_loop
from websocket_feed import start_websocket_feed

client = FakeBinanceClient()
current_strategy = "basic"

def main_loop():
    global current_strategy
    while True:
        current_strategy = select_strategy()
        run_trading_loop(client, current_strategy)
        time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=start_websocket_feed, daemon=True).start()
    threading.Thread(target=start_scheduler, daemon=True).start()
    main_loop()


import asyncio
import random
from datetime import datetime
import websockets
import json

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "AVAXUSDT", "MATICUSDT"]
SPEND_PER_TRADE = 50.0

trade_count = 0

async def simulate_trade(symbol, price):
    global trade_count
    quantity = SPEND_PER_TRADE / float(price)
    trade_count += 1
    print(f"[{datetime.utcnow()}] 🔥 TRADE #{trade_count}: {symbol} @ ${price} | Qty: {quantity:.4f}")

async def handle_price_update(symbol, price):
    # Handler hver 5. sekund - superaggressiv: kjøp alltid for test
    await simulate_trade(symbol, price)

async def connect_ws(symbol):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            json_data = json.loads(data)
            price = json_data["p"]
            await handle_price_update(symbol.upper(), price)
            await asyncio.sleep(5)  # Superhøy frekvens

async def main():
    await asyncio.gather(*(connect_ws(sym) for sym in SYMBOLS))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot manually stopped.")
def run_aggressive_strategy():
            import asyncio 
            asyncio.run(main())        

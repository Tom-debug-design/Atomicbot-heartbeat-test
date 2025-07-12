
import asyncio
import websockets
import json
import time

# Globale priser fra Binance WebSocket
live_prices = {}

# Tokens å overvåke
tokens = ["btcusdt", "ethusdt", "bnbusdt"]

async def fetch_prices():
    uri = f"wss://stream.binance.com:9443/stream?streams={'/'.join([t + '@trade' for t in tokens])}"
    async with websockets.connect(uri) as ws:
        while True:
            try:
                msg = await ws.recv()
                data = json.loads(msg)
                stream = data.get("stream", "")
                symbol = stream.split("@")[0]
                price = float(data["data"]["p"])
                live_prices[symbol.upper()] = price
            except Exception as e:
                print(f"[WebSocket error] {e}")
                await asyncio.sleep(5)

async def scalper_loop():
    portfolio = {}
    trade_log = []

    while True:
        for symbol in tokens:
            pair = symbol.upper()
            price = live_prices.get(pair)
            if not price:
                continue

            # Entry condition (simplified demo)
            if pair not in portfolio:
                qty = round(50 / price, 6)
                portfolio[pair] = {"entry": price, "qty": qty}
                print(f"BUY {pair} @ ${price:.2f} | Qty: {qty}")
                trade_log.append((time.time(), pair, "BUY", price, qty))
            else:
                # Exit logic: take 1% profit or 1% loss
                entry = portfolio[pair]["entry"]
                change = (price - entry) / entry
                if abs(change) >= 0.01:
                    print(f"SELL {pair} @ ${price:.2f} | PnL: {change*100:.2f}%")
                    del portfolio[pair]
                    trade_log.append((time.time(), pair, "SELL", price, change))

        await asyncio.sleep(5)

async def main():
    await asyncio.gather(
        fetch_prices(),
        scalper_loop(),
    )

if __name__ == "__main__":
    asyncio.run(main())

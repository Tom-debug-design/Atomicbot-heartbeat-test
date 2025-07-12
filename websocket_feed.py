import json
import threading
import websocket

live_prices = {}

def on_message(ws, message):
    data = json.loads(message)
    symbol = data["s"]
    price = float(data["p"])
    live_prices[symbol] = price

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def start_websocket_feed():
    def run():
        symbols = ["btcusdt", "ethusdt", "bnbusdt"]
        stream = "/".join([f"{s}@trade" for s in symbols])
        url = f"wss://stream.binance.com:9443/stream?streams={stream}"
        ws = websocket.WebSocketApp(url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)
        ws.run_forever()
    threading.Thread(target=run, daemon=True).start()

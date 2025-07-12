import json
import time
import websocket
import threading

# Live price storage
latest_prices = {}

# Callback functions for websocket events
def on_message(ws, message):
    data = json.loads(message)
    if 's' in data and 'c' in data:
        symbol = data['s']
        price = float(data['c'])
        latest_prices[symbol] = price
        print(f"Price update: {symbol} = {price}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket connection opened")
    payload = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@ticker",
            "ethusdt@ticker",
            "bnbusdt@ticker"
        ],
        "id": 1
    }
    ws.send(json.dumps(payload))

def start_websocket():
    url = "wss://stream.binance.com:9443/ws"
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

# Start the WebSocket in a separate thread
thread = threading.Thread(target=start_websocket)
thread.daemon = True
thread.start()

# Main logic example (mock strategy)
while True:
    for symbol, price in latest_prices.items():
        print(f"[{symbol}] Latest price: {price}")
    time.sleep(10)
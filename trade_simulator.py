import requests
from discord_logger import send_discord_message

TOKENS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'SOLUSDT', 'AVAXUSDT', 'MATICUSDT']
USDT_BALANCE = 1000
TRADE_SIZE_PERCENT = 5

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    response = requests.get(url)
    return float(response.json()['price'])

def simulate_trades():
    for symbol in TOKENS:
        try:
            price = get_price(symbol)
            amount_usdt = USDT_BALANCE * (TRADE_SIZE_PERCENT / 100)
            qty = round(amount_usdt / price, 6)
            message = f"💰 Simulated BUY: {symbol} at ${price:,.2f} | Amount: ${amount_usdt:.2f} | Qty: {qty}"
            send_discord_message(message)
        except Exception as e:
            print(f"Failed trade for {symbol}: {e}")

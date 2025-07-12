from websocket_feed import live_prices

class FakeBinanceClient:
    def __init__(self):
        self.positions = {}

    def get_price(self, symbol):
        return live_prices.get(symbol, 100.0)

    def order_market_buy(self, symbol, quantity):
        price = self.get_price(symbol)
        self.positions[symbol] = (price, quantity)
        return { "symbol": symbol, "price": price, "qty": quantity }

    def order_market_sell(self, symbol, quantity):
        if symbol not in self.positions:
            return None
        entry_price, qty = self.positions.pop(symbol)
        exit_price = self.get_price(symbol)
        pnl = (exit_price - entry_price) * quantity
        return { "symbol": symbol, "entry": entry_price, "exit": exit_price, "pnl": pnl }

def run_trading_loop(client, strategy):
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    for symbol in symbols:
        if symbol in client.positions:
            entry_price, qty = client.positions[symbol]
            current_price = client.get_price(symbol)
            if current_price >= entry_price * 1.01 or current_price <= entry_price * 0.99:
                result = client.order_market_sell(symbol, qty)
                print(f"EXIT [{strategy}] {symbol} | Entry: ${entry_price:.2f} → Exit: ${result['exit']:.2f} | PnL: ${result['pnl']:.2f}")
        else:
            price = client.get_price(symbol)
            qty = round(50 / price, 4)
            result = client.order_market_buy(symbol, qty)
            print(f"ENTRY [{strategy}] {symbol} @ ${price:.2f} | Qty: {qty}")

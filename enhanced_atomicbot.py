
# AtomicBot Enhancements - Strategy Logging and Aggression Control

import logging
from datetime import datetime

# Global state
trade_log = []
strategy_log = {}
last_summary_hour = None

# Simulated trading function with logging
def perform_trade(strategy, symbol, price, quantity):
    trade = {
        "timestamp": datetime.utcnow().isoformat(),
        "strategy": strategy,
        "symbol": symbol,
        "price": price,
        "quantity": quantity,
        "pnl": 0.0  # Placeholder for PnL simulation
    }
    trade_log.append(trade)
    strategy_log[strategy] = strategy_log.get(strategy, 0) + 1
    logging.info(f"TRADE EXECUTED: {strategy} | {symbol} @ {price} | Qty: {quantity}")

# Price update simulation
def on_price_update(symbol, price):
    logging.info(f"PRICE UPDATE: {symbol} = {price}")
    # Simulate a trigger
    if price % 2 == 0:
        perform_trade("even_minute", symbol, price, 0.01)
    else:
        perform_trade("basic", symbol, price, 0.01)

# Hourly reporting function
def hourly_report():
    from collections import defaultdict
    from datetime import datetime

    now = datetime.utcnow()
    report = defaultdict(lambda: {"trades": 0, "volume": 0})
    for trade in trade_log:
        strategy = trade["strategy"]
        report[strategy]["trades"] += 1
        report[strategy]["volume"] += trade["price"] * trade["quantity"]

    total_trades = sum(r["trades"] for r in report.values())
    total_volume = sum(r["volume"] for r in report.values())
    logging.info("---- HOURLY REPORT ----")
    logging.info(f"Total trades: {total_trades}")
    logging.info(f"Total simulated spend: ${total_volume:.2f}")
    for strat, stats in report.items():
        logging.info(f"Strategy '{strat}': {stats['trades']} trades | Spend: ${stats['volume']:.2f}")

# Simulated daily report (at 06:00 UTC)
def daily_report():
    hourly_report()
    # Placeholder: more stats and summaries can be added here
    logging.info("✅ Daily report complete.")

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Example test run
on_price_update("BTCUSDT", 117760)
on_price_update("ETHUSDT", 2950)
on_price_update("BNBUSDT", 690)
hourly_report()

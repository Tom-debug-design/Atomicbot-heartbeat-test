# AtomicBot (Simulated Trades + Heartbeat)

Sends heartbeat and simulated trades to Discord using public Binance prices.

## Includes
- `main.py`: Runs Flask + loop
- `discord_logger.py`: Sends messages to Discord
- `trade_simulator.py`: Runs 5% simulated buy per token
- `requirements.txt`, `Procfile`

## Deployment
Use Railway. Set `DISCORD_WEBHOOK` as environment variable.


def report_pnl(hourly=False, daily=False):
    if daily:
        print("📝 Daily PnL Report: [Simulated]")
    elif hourly:
        print("📊 Hourly PnL Report: [Simulated]")
    else:
        print("🔍 General PnL Report")

def log_trade(trade):
    print(f"🔁 Trade logged: {trade}")

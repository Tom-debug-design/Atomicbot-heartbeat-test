from datetime import datetime

def report_pnl(hourly=False, daily=False):
    now = datetime.utcnow()
    if daily:
        print(f"[📝 Daily Report] Generated at {now}")
    elif hourly:
        print(f"[📊 Hourly Report] Generated at {now}")
    else:
        print(f"[🔍 General PnL Report] at {now}")

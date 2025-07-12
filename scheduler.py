import schedule, time

def hourly_report():
    print("📊 Hourly report: summary (to be improved with strategy PnL data)")

def start_scheduler():
    schedule.every().hour.at(":00").do(hourly_report)
    while True:
        schedule.run_pending()
        time.sleep(1)

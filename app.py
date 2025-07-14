from flask import Flask
from discord_logger import send_discord_message
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return "AtomicBot is running."

@app.route("/heartbeat")
def heartbeat():
    try:
        send_discord_message("💓 Heartbeat: AtomicBot is alive and kicking!")
        return "Heartbeat sent!"
    except Exception as e:
        print("🚨 Heartbeat-feil:", e)
        return f"Discord error: {e}"

# Rapportfunksjoner med try/except-logging
def hourly_report():
    try:
        now = datetime.datetime.now(timezone('Europe/Oslo'))
        report = f"⏰ Timesrapport: {now.strftime('%Y-%m-%d %H:00')}"
        send_discord_message(report)
    except Exception as e:
        print("🚨 Feil i hourly_report:", e)

def daily_report():
    try:
        now = datetime.datetime.now(timezone('Europe/Oslo'))
        report = f"📅 Dagsrapport: {now.strftime('%Y-%m-%d')}"
        send_discord_message(report)
    except Exception as e:
        print("🚨 Feil i daily_report:", e)

# Start scheduler med feiltoleranse
try:
    scheduler = BackgroundScheduler(timezone=timezone('Europe/Oslo'))
    scheduler.add_job(hourly_report, 'cron', minute=0)
    scheduler.add_job(daily_report, 'cron', hour=6, minute=0)
    scheduler.start()
except Exception as e:
    print("🚨 Klarte ikke starte scheduler:", e)

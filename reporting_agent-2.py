
import requests
from datetime import datetime, timezone
import time

WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # Sett inn din webhook

def send_report():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    message = {
        "content": f"🕒 Timesrapport: AtomicBot er fortsatt i live kl {now} UTC!"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 204:
            print(f"✅ Timesrapport sendt: {now}")
        else:
            print(f"❌ Feil ved sending ({response.status_code}): {response.text}")
    except Exception as e:
        print("Webhook-feil:", e)

if __name__ == "__main__":
    while True:
        current_minute = datetime.now(timezone.utc).minute
        if current_minute == 0:
            send_report()
            time.sleep(60)
        time.sleep(10)

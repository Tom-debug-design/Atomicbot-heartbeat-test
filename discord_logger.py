import requests

# ⛔ VIKTIG: BYTT UT DENNE MED DIN EGEN WEBHOOK-URL FRA DISCORD
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # <- Sett inn din egen her

MAX_LENGTH = 1900

def send_discord_message(message):
    if not message:
        return

    try:
        if len(message) <= MAX_LENGTH:
            _send(message)
        else:
            parts = [message[i:i+MAX_LENGTH] for i in range(0, len(message), MAX_LENGTH)]
            for part in parts:
                _send(part)
    except Exception as e:
        print("🚨 Discord-feil:", e)

def _send(text):
    r = requests.post(DISCORD_WEBHOOK_URL, json={"content": text})
    if r.status_code not in (200, 204):
        print(f"🚨 Webhook-feil: {r.status_code} | {r.text}")

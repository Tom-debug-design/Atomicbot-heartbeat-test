import requests

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/139185593071560735/uH6LYuqM6uHLet9KhsgCS89fQikhyuPRJm..."

def send_discord_message(message):
    if not message:
        return
    try:
        data = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"Failed to send message: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception during sending message: {e}")
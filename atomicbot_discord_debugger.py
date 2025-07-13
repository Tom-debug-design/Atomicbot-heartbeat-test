
import os
import asyncio
import logging
import aiohttp

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

logging.basicConfig(level=logging.INFO)

async def send_discord_message(channel_id, message):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }
    json_data = {
        "content": message
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as resp:
            logging.info(f"Discord response status: {resp.status}")
            text = await resp.text()
            logging.info(f"Discord response text: {text}")
            if resp.status != 200 and resp.status != 204:
                raise Exception("Failed to send Discord message")

async def main():
    if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID:
        logging.error("Missing DISCORD_TOKEN or DISCORD_CHANNEL_ID in environment variables.")
        return
    try:
        await send_discord_message(DISCORD_CHANNEL_ID, "✅ Discord testmelding: Bot er live og sender!")
        logging.info("Testmelding sendt til Discord.")
    except Exception as e:
        logging.error(f"Feil ved sending til Discord: {e}")

if __name__ == "__main__":
    asyncio.run(main())

# AtomicBot Heartbeat

Simple Flask app that sends a heartbeat message to Discord every 60 seconds.

## Files
- `main.py`: Runs the Flask server and heartbeat loop.
- `discord_logger.py`: Handles Discord webhook messages.
- `requirements.txt`: Dependencies.
- `Procfile`: Launches the app via Gunicorn.

## Deployment
Deploy to Railway or similar platform. Make sure to set `DISCORD_WEBHOOK_URL` as an environment variable.

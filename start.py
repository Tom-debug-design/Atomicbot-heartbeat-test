import time
from bridge_agent import run_bridge
from reporter_hourly import run_hourly_reporter

if __name__ == "__main__":
    run_bridge()
    run_hourly_reporter()

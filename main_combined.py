
import threading
import time
from aggressive_atomicbot import run_aggressive_strategy
from atomicbot_dispatch_goal import run_goal_dispatch
from atomicbot_discord_debugger import run_discord_logger

def main():
    try:
        # Start aggressive trading strategy
        aggressive_thread = threading.Thread(target=run_aggressive_strategy)
        aggressive_thread.start()

        # Start goal-based dispatch
        goal_thread = threading.Thread(target=run_goal_dispatch)
        goal_thread.start()

        # Start Discord logging
        discord_thread = threading.Thread(target=run_discord_logger)
        discord_thread.start()

        # Keep the main thread alive
        while True:
            time.sleep(10)

    except Exception as e:
        print(f"[ERROR] Exception in main_combined.py: {e}")

if __name__ == "__main__":
    main()

# Unified startup for AtomicBot system
import os
from atomicbot_v3 import main as bot_main
from reporter_hourly import reporter
from bridge_agent import bridge_agent

if __name__ == '__main__':
    print('Starting AtomicBot Full System')
    bot_main.main()
    reporter.main()
    bridge_agent.main()

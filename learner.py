import json
import os
import random

SIGNAL_LOG = "signals_log.json"

def log_signal(symbol, rsi, ema_diff, price, result=None):
    entry = {
        "symbol": symbol,
        "rsi": rsi,
        "ema_diff": ema_diff,
        "price": price,
        "timestamp": datetime.utcnow().isoformat(),
        "result": result
    }
    data = []
    if os.path.exists(SIGNAL_LOG):
        with open(SIGNAL_LOG, "r") as f:
            data = json.load(f)
    data.append(entry)
    with open(SIGNAL_LOG, "w") as f:
        json.dump(data, f, indent=2)

def get_token_priority(tokens):
    # Placeholder: random shuffle simulerer læring
    ranked = tokens[:]
    random.shuffle(ranked)
    return ranked

# strategies.py

def check_buy_signal(df):
    try:
        if df.shape[1] < 6:
            return False
        last_rsi = df.iloc[-1].get("rsi", 50)
        last_price = df.iloc[-1].get("price", 0)
        if last_rsi < 30:
            return True
        return False
    except Exception as e:
        print("Strategy error:", e)
        return False


def select_strategy(): return 'aggressive_only'
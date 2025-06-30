import requests
import pandas as pd

def fetch_live_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if isinstance(data, dict) and "price" in data:
            return float(data["price"])
        else:
            raise ValueError(f"Unexpected response: {data}")
    except Exception as e:
        print(f"[ERROR] fetch_live_price: {e}")
        return None  # Show 'Fetching failed' in Streamlit

def calculate_indicators():
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
    try:
        raw_data = requests.get(url, timeout=10).json()
        if not isinstance(raw_data, list) or len(raw_data) == 0:
            raise ValueError("Binance API returned no kline data.")

        df = pd.DataFrame(raw_data)[[0, 1, 2, 3, 4]]
        df.columns = ['time', 'open', 'high', 'low', 'close']
        df['close'] = df['close'].astype(float)

        # RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_value = rsi.iloc[-1] if not rsi.isnull().all() else 50

        # MACD
        ema12 = df['close'].ewm(span=12).mean()
        ema26 = df['close'].ewm(span=26).mean()
        macd_value = (ema12 - ema26).iloc[-1]

        # Bollinger %B
        ma20 = df['close'].rolling(20).mean()
        std = df['close'].rolling(20).std()
        upper = ma20 + 2 * std
        lower = ma20 - 2 * std
        bb_value = (df['close'].iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1])

        return round(rsi_value, 2), round(macd_value, 2), round(bb_value, 2)

    except Exception as e:
        print(f"[ERROR] calculate_indicators: {e}")
        return 50, 0, 0.5  # Safe default values


def make_prediction(current_price, target_price, rsi, macd, bb):
    score = 0
    if rsi < 70 and rsi > 50:
        score += 1
    if macd > 0:
        score += 1
    if bb > 0.5:
        score += 1
    if current_price < target_price:
        score += 1
    return "YES" if score >= 3 else "NO"

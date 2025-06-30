import streamlit as st
import datetime
from utils import fetch_live_price, calculate_indicators, make_prediction

st.set_page_config(page_title="BTC Price Predictor", layout="centered")

st.title("📈 BTC Price Prediction Tool")

# Input form
st.subheader("Enter Prediction Parameters")
target_price = st.number_input("🎯 Target Price (USDT)", value=30000.0)
target_time = st.time_input("🕒 Target Time", value=datetime.datetime.now().time())

# Live Price
price = fetch_live_price()
if price:
    st.markdown(f"**📊 Live BTC Price:** ${price:.2f}")
else:
    st.warning("⚠️ Failed to fetch live price from Binance.")

# Indicators
rsi, macd, bb = calculate_indicators()
st.markdown(f"**📉 RSI:** {rsi:.2f} | **MACD:** {macd:.2f} | **BB %B:** {bb:.2f}")

# Prediction
if st.button("🔮 Predict"):
    decision = make_prediction(price, target_price, rsi, macd, bb)
    if decision == "YES":
        st.success("✅ Predicted: Price will be ABOVE target.")
    else:
        st.error("❌ Predicted: Price will be BELOW target.")

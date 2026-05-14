import streamlit as st
from data.fetcher import fetch_stock_data
from models.forecaster import train_model, forecast_next_day
from indicators.technical import add_all_indicators
from ui.charts import plot_candlestick, plot_rsi, plot_macd
from ai.insights import generate_insights

st.set_page_config(page_title="Stock Analysis Platform", layout="wide")

st.title("📈 Stock Analysis Platform")
st.sidebar.header("Configuration")

ticker = st.sidebar.text_input("Enter Stock Ticker", value="RELIANCE.NS")
period_days = st.sidebar.slider("Historical Data Period (days)", min_value=365, max_value=3650, value=1825, step=365)
analyse_button = st.sidebar.button("Analyse Stock")

if analyse_button:
    with st.spinner("Fetching Data and running Analysis...."):
        # 1 - Fetch data
        df = fetch_stock_data(ticker, period_days)

        if df.empty:
            st.error("Could not fetch data. Please check the ticker symbol.")
        else:
            # 2 - Add indicators
            df = add_all_indicators(df)

            # 3 - Train model
            result = train_model(df)

            # 4 - Forecast next day
            forecast_price = forecast_next_day(result['model'], df)

            # --- Metrics Row ---
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Current Price", f"₹{df['Close'].iloc[-1]:.2f}")

            with col2:
                st.metric("Forecast Price", f"₹{forecast_price:.2f}")

            with col3:
                st.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")

            # --- Charts ---
            st.subheader("📊 Price Chart")
            st.plotly_chart(plot_candlestick(df, ticker), use_container_width=True)

            st.subheader("📉 RSI Indicator")
            st.plotly_chart(plot_rsi(df), use_container_width=True)

            st.subheader("📈 MACD Indicator")
            st.plotly_chart(plot_macd(df), use_container_width=True)

            # --- AI Insights ---
            st.subheader("🤖 AI Market Insights")
            insights = generate_insights(
                ticker=ticker,
                current_price=df['Close'].iloc[-1],
                rsi=df['RSI'].iloc[-1],
                macd=df['MACD'].iloc[-1],
                forecast_price=forecast_price,
                feature_importance=result['feature_importance'].index[0]
            )
            st.markdown(insights)

            # --- Feature Importance ---
            st.subheader("🔍 Why This Trend?")
            st.bar_chart(result['feature_importance'])

            # --- Model Performance ---
            st.caption(f"Model MAE: ₹{result['mae']} | R²: {result['r2']} | Data points: {len(df)}")

            # --- Disclaimer ---
            st.warning("⚠️ This platform is for educational purposes only. Not a financial advice. Always do your own research.")
            
            
            
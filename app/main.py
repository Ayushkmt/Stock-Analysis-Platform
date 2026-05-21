import streamlit as st
from data.fetcher import fetch_stock_data
from models.forecaster import train_model, forecast_next_day
from indicators.technical import add_all_indicators
from ui.charts import plot_candlestick, plot_rsi, plot_macd
from ai.insights import generate_insights

st.set_page_config(page_title="Stock Analysis Platform", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .main-header {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .metric-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }

        .stButton>button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            width: 100%;
        }

        .stButton>button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Stock Analysis Platform")
st.markdown("""
    <div class='main-header'>
        <h1>📈 Stock Analysis Platform</h1>
        <p style='color: #666; font-size: 1.1rem;'>
            AI-powered stock analysis and forecasting for Indian markets (NSE)
        </p>
    </div>
""", unsafe_allow_html=True)

st.info("""
**What this platform provides:**
📊 Live stock data and interactive charts 
📉 Technical indicators — SMA, EMA, RSI, MACD
🤖 ML-based next day price forecast
💡 AI generated market insights via Gemini
🔎 Explainable predictions with feature importance
""")

st.warning("⚠️ For educational purposes only. Not financial advice.")

st.markdown("---")

st.sidebar.header("Configuration")
st.sidebar.subheader("Quick Select")
quick_select = st.sidebar.selectbox(
    "Popular Indian Stocks",
    ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS", "ADANIENT.NS", "BAJFINANCE.NS"]
)

st.sidebar.subheader("Or Enter Manually")
ticker = st.sidebar.text_input("Stock Ticker", value=quick_select)
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

            current_price = df['Close'].iloc[-1]
            previous_price = df['Close'].iloc[-2]
            price_delta = current_price - previous_price

            with col1:
                st.metric(
                    "Current Price",
                    f"₹{current_price:.2f}",
                    delta=f"₹{price_delta:.2f} from yesterday"
            )
            
            with col2:
                st.metric("Forecast Price", f"₹{forecast_price:.2f}")

            rsi_value = df['RSI'].iloc[-1]
            if rsi_value > 70:
                rsi_label = "Overbought 🔴"
            elif rsi_value < 30:
                rsi_label = "Oversold 🟢"
            else:
                rsi_label = "Neutral 🟡"

            with col3:
                st.metric("RSI", f"{rsi_value:.2f}", delta=rsi_label)
                
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
            st.subheader("Why This Trend?")
            st.bar_chart(result['feature_importance'])

            # --- Model Performance ---
            r2 = result['r2']
            if r2 > 0.8:
                model_quality = "Strong 🟢"
            elif r2 > 0.5:
                model_quality = "Moderate 🟡"
            else:
                model_quality = "Weak 🔴"
                
            st.caption(
                f"Model Accuracy: {model_quality} | "
                f"MAE: ₹{result['mae']} | "
                f"R²: {result['r2']} | "
                f"Data points: {len(df)}"
                )

            # --- Disclaimer ---
            st.warning("⚠️ This platform is for educational purposes only. Not a financial advice. Always do your own research.")
            
            
            
            
            
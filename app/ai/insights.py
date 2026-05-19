import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env from project root
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / '.env')

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

def build_prompt(ticker, current_price, rsi, macd, forecast_price, feature_importance):
    prompt = f"""
    You are a stock market analyst.

    Analyze the following data for {ticker}:
    - Current Price: ₹{current_price:.2f}
    - RSI: {rsi:.2f}
    - MACD: {macd:.2f}
    - Forecasted Price for Tomorrow: ₹{forecast_price}
    - Most Influential Indicator: {feature_importance}

    Provide:
    1. A brief market summary based on the indicators.
    2. What the trend suggests (bullish, bearish, or neutral).
    3. A disclaimer that this is not financial advice and markets are unpredictable.

    Keep it concise and easy to understand. Use simple language.
    """
    return prompt


def generate_insights(ticker, current_price, rsi, macd, forecast_price, feature_importance):
    """
    Generates AI market insights using Gemini API.
    Falls back to mock response if API call fails.
    """
    try:
        prompt = build_prompt(
            ticker, current_price, rsi,
            macd, forecast_price, feature_importance
        )

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        # Fallback mock response if API fails
        return f"""
        **Market Summary:**
        {ticker} is currently trading at ₹{current_price:.2f}.
        RSI at {rsi:.2f} suggests neutral momentum.

        **Trend Analysis:**
        Forecasted price for tomorrow is ₹{forecast_price}.

        **Disclaimer:**
        This analysis is for educational purposes only.
        Not financial advice. Always do your own research.

        _(AI insights unavailable: {str(e)})_
        """



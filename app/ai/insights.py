def build_Prompt(Ticker, current_price, rsi, macd, forecast_price, feature_importance):
    prompt = f"""
    You are a stock market analyst. 
    
    Analyze the following data for {Ticker}:
    - Current Price: ₹{current_price}
    - RSI: {rsi:.2f}
    - MACD: {macd:.2f}
    - Forecasted Price for Tomorrow: ₹{forecast_price}
    - Most Influential Indicator: {feature_importance}
    
    Provide:
    1. A Brief market summary based on the indicators.
    2. What the trend suggests (bullish, bearish, or neutral).
    3. Disclaimer that this is not financial advice and to do their own research.
    
    Keep the analysis concise (2-3 sentences) and easy to understand for a general audience.
    
    """
    return prompt

def generate_insight(ticker, current_price, rsi, macd, forecast_price, feature_importance):
    """
    Generates AI market insights.
    Currently returns a mock response.
    Gemini API will be swapped in here later — one function change.
    """
    prompt = build_prompt(ticker, current_price, rsi, macd, forecast_price, feature_importance)

    # --- MOCK RESPONSE (Gemini swap goes here later) ---
    mock_response = f"""
    **Market Summary:**
    {ticker} is currently trading at ₹{current_price:.2f}. 
    Based on technical indicators, the stock shows moderate activity 
    with RSI at {rsi:.2f} suggesting neutral momentum.

    **Trend Analysis:**
    The MACD value of {macd:.2f} and the dominance of {feature_importance} 
    as the key indicator suggest a cautiously bullish outlook. 
    Forecasted price for tomorrow is ₹{forecast_price}.

    **Disclaimer:**
    This analysis is for educational purposes only and does not 
    constitute financial advice. Stock markets are inherently unpredictable. 
    Always do your own research before making investment decisions.
    """
    return 



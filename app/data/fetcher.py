import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(ticker: str, period_days: int = 1825) -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        ticker: Stock symbol e.g. 'RELIANCE.NS', 'TCS.NS'
        period_days: How many days of history to fetch (default: 1 year)

    Returns:
        DataFrame with OHLCV data or empty DataFrame on failure
    """
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=period_days)

        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(start=start_date, end=end_date)

        # If data is empty, ticker is likely wrong
        if df.empty:
            return pd.DataFrame()

        # Reset index so 'Date' becomes a regular column
        df.reset_index(inplace=True)

        # Keep only the columns we need
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

        # Remove timezone info from Date column (causes issues later)
        df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)

        return df
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()
    
    
import pandas as pd


def calculate_sma(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Simple Moving Average - smooths price data over N days.
    Above SMA = uptrend, Below SMA = downtrend.
    """
    return df['Close'].rolling(window=period).mean()


def calculate_ema(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """
    Exponential Moving Average - gives more weight to recent prices.
    Reacts faster to price changes than SMA.
    """
    return df['Close'].ewm(span=period, adjust=False).mean()


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    RSI between 0-100.
    Above 70 = overbought (possible drop).
    Below 30 = oversold (possible rise).
    """
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(df: pd.DataFrame):
    """
    MACD = 12day EMA - 26day EMA.
    Signal line = 9day EMA of MACD.
    When MACD crosses above signal = bullish. Below = bearish.
    """
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()

    macd_line = ema_12 - ema_26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Master function - adds all indicators to the DataFrame at once.
    This is what we call from the rest of the app.
    """
    df = df.copy()  # never mutate the original DataFrame

    df['SMA_20'] = calculate_sma(df, 20)
    df['SMA_50'] = calculate_sma(df, 50)
    df['EMA_20'] = calculate_ema(df, 20)
    df['RSI'] = calculate_rsi(df)

    df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = calculate_macd(df)

    return df
    
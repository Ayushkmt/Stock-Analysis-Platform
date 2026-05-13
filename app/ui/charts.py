import plotly.graph_objects as go

def plot_candlestick(df, ticker):
    """Candlestick chart showing Open, High, Low, Close prices."""
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=ticker
    )])

    fig.update_layout(
        title=f'{ticker} - Price Chart',
        yaxis_title='Price (₹)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False,  # cleaner look without range slider
        template='plotly_dark',
        height=500
    )
    return fig

def plot_rsi(df):
    """RSI chart with overbought/oversold threshold lines."""
    fig = go.Figure()

    # RSI line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['RSI'],
        name='RSI',
        line=dict(color='purple', width=1.5)
    ))

    # Overbought line at 70
    fig.add_hline(y=70, line_dash='dash',
                  line_color='red', annotation_text='Overbought (70)')

    # Oversold line at 30
    fig.add_hline(y=30, line_dash='dash',
                  line_color='green', annotation_text='Oversold (30)')

    fig.update_layout(
        title='RSI - Relative Strength Index',
        yaxis_title='RSI Value',
        xaxis_title='Date',
        template='plotly_dark',
        height=300
    )
    return fig

def plot_macd(df):
    """MACD chart with MACD line, Signal line, and Histogram."""
    fig = go.Figure()

    # MACD line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['MACD'],
        name='MACD',
        line=dict(color='blue', width=1.5)
    ))
    # Signal line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['MACD_Signal'],
        name='Signal',
        line=dict(color='orange', width=1.5)
    ))
    # Histogram
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['MACD_Histogram'],
        name='Histogram',
        marker_color='grey'
    ))

    fig.update_layout(
        title='MACD - Moving Average Convergence Divergence',
        yaxis_title='MACD Value',
        xaxis_title='Date',
        template='plotly_dark',
        height=300
    )
    return fig
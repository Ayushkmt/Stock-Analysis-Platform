import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Features we feed into the model
FEATURE_COLUMNS = ['SMA_20', 'SMA_50', 'EMA_20', 'RSI', 'MACD', 'MACD_Signal']

def prepare_data(df: pd.DataFrame):
    """
    Prepares features and target from DataFrame.
    Target is next day's Close price (shifted by 1).
    """
    df = df.copy()

    # Target = tomorrow's closing price
    # shift(-1) moves values up by one row — so today's row gets tomorrow's price
    df['Target'] = df['Close'].shift(-1)

    # Drop last row since it has no target (no tomorrow)
    df.dropna(inplace=True)

    X = df[FEATURE_COLUMNS]
    y = df['Target']

    return X, y

def train_model(df: pd.DataFrame):
    """
    Trains Random Forest model on historical stock data.
    Splits chronologically — never randomly shuffle time series data.
    
    Returns model, predictions, actual values, and feature importances.
    """
    X, y = prepare_data(df)

    # Chronological split — 80% train, 20% test
    # Why not train_test_split? Because that shuffles data randomly
    # For stock data, past trains future — never the other way
    split_index = int(len(X) * 0.8)

    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions on test data
    predictions = model.predict(X_test)

    # Model performance metrics
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Feature importance — which indicator influenced predictions most
    feature_importance = pd.Series(
        model.feature_importances_,
        index=FEATURE_COLUMNS
    ).sort_values(ascending=False)
    return {
        "model": model,
        "predictions": predictions,
        "actual": y_test.values,
        "dates": df['Date'].iloc[split_index:].values,
        "mae": round(mae, 2),
        "r2": round(r2, 4),
        "feature_importance": feature_importance
    }

def forecast_next_day(model, df: pd.DataFrame) -> float:
    """
    Predicts next day's closing price using the latest indicator values.
    """
    latest = pd.DataFrame([df[FEATURE_COLUMNS].iloc[-1]], columns=FEATURE_COLUMNS)
    predicted_price = model.predict(latest)[0]
    return round(predicted_price, 2)


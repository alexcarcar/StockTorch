import warnings

warnings.filterwarnings("ignore")

import os
import datetime as dt
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import joblib

# USER SETTINGS
TICKER = "GWRE"
HISTORY_YEARS = 15  # use more historical data (set to e.g. 15 years)
LAGS = 30  # more lag features
TEST_RATIO = 0.12  # smaller test set -> more training data
RANDOM_STATE = 42
MODEL_PATH = "gwre_model.joblib"
SCALER_PATH = "gwre_scaler.joblib"
PLOT_PATH = "gwre_predictions.png"


def start_date_from_years(years):
    today = dt.date.today()
    return (today - dt.timedelta(days=365 * years)).isoformat()


START = start_date_from_years(HISTORY_YEARS)
END = None  # up to today


def download_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        raise RuntimeError(f"No data for {ticker} in range {start}..{end}")
    return df


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / (avg_loss + 1e-12)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def create_features(df, lags=30):
    df = df.copy()
    # ensure common column names are strings
    df.columns = [str(c) for c in df.columns]
    # detect close-like column
    close_col = next((c for c in df.columns if "close" in c.lower()), None)
    if close_col is None:
        raise RuntimeError(f"No close-like column found. Columns: {list(df.columns)[:20]}")

    # basic features
    df["Return"] = df[close_col].pct_change()
    df["MA5"] = df[close_col].rolling(5).mean()
    df["MA10"] = df[close_col].rolling(10).mean()
    df["MA20"] = df[close_col].rolling(20).mean()

    # EMA and MACD
    df["EMA12"] = df[close_col].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df[close_col].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]

    # RSI
    df["RSI14"] = compute_rsi(df[close_col], period=14)

    # Bollinger Bands (20,2)
    ma20 = df[close_col].rolling(20).mean()
    std20 = df[close_col].rolling(20).std()
    df["BB_upper"] = ma20 + 2 * std20
    df["BB_lower"] = ma20 - 2 * std20
    df["BB_width"] = (df["BB_upper"] - df["BB_lower"]) / (ma20 + 1e-12)

    # Volatility
    df["Volatility_5"] = df["Return"].rolling(5).std()

    # Lag features for close
    for lag in range(1, lags + 1):
        df[f"lag_{lag}"] = df[close_col].shift(lag)

    # Target: next-day close
    df["target"] = df[close_col].shift(-1)

    df = df.dropna()
    return df


def time_split(df, test_ratio=0.2):
    n = len(df)
    split = int(n * (1 - test_ratio))
    train = df.iloc[:split]
    test = df.iloc[split:]
    return train, test


def expanding_ensemble_predict(train_df, test_df, feature_cols, random_state=42, n_splits=4):
    """
    Train several models on expanding slices of the training history and average predictions.
    This lets later predictions leverage models trained on different historical extents.
    """
    models = []
    scalers = []
    n = len(train_df)
    # compute split indices that grow: e.g., 25%, 50%, 75%, 100% of training data
    split_points = [int(n * (i / n_splits)) for i in range(1, n_splits + 1)]
    # ensure monotonic and > minimal size
    split_points = sorted(set([max(10, p) for p in split_points if p > 10]))

    for end_idx in split_points:
        sub = train_df.iloc[:end_idx]
        X = sub[feature_cols].values
        y = sub["target"].values
        scaler = StandardScaler().fit(X)
        Xs = scaler.transform(X)
        model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=random_state, n_jobs=-1)
        model.fit(Xs, y)
        models.append(model)
        scalers.append(scaler)

    # produce predictions from each model and average
    X_test = test_df[feature_cols].values
    preds_list = []
    for model, scaler in zip(models, scalers):
        preds = model.predict(scaler.transform(X_test))
        preds_list.append(preds)
    if not preds_list:
        # fallback: train single model on full train
        scaler = StandardScaler().fit(train_df[feature_cols].values)
        model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=random_state, n_jobs=-1)
        model.fit(scaler.transform(train_df[feature_cols].values), train_df["target"].values)
        preds = model.predict(scaler.transform(X_test))
        return model, scaler, preds

    preds_avg = np.mean(preds_list, axis=0)
    # return last model/scaler as representative too
    return models[-1], scalers[-1], preds_avg


def plot_results(test_df, preds, save_path):
    plt.figure(figsize=(12, 6))
    # detect display close column
    close_col = next((c for c in test_df.columns if "close" in c.lower()), "Close")
    plt.plot(test_df.index, test_df["target"], label="Actual Next Close", linewidth=1.5)
    plt.plot(test_df.index, preds, label="Predicted Next Close", linewidth=1.2)
    plt.title(f"{TICKER} Actual vs Predicted Next-Day Close")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main():
    df = download_data(TICKER, START, END)
    df = create_features(df, lags=LAGS)

    # select features present in df
    desired = [f"lag_{i}" for i in range(1, LAGS + 1)] + ["MA5", "MA10", "MA20",
                                                          "Volatility_5", "EMA12", "EMA26",
                                                          "MACD", "RSI14", "BB_width", "Return"]
    feature_cols = [c for c in desired if c in df.columns]
    if not feature_cols:
        raise RuntimeError("No feature columns found after feature creation.")

    train, test = time_split(df, TEST_RATIO)
    if len(train) < 30 or len(test) < 5:
        raise RuntimeError(f"Insufficient data after split: train={len(train)}, test={len(test)}")

    # train expanding-window ensemble and predict
    model, scaler, preds = expanding_ensemble_predict(train, test, feature_cols, RANDOM_STATE, n_splits=4)

    mae = mean_absolute_error(test["target"].values, preds)
    rmse = mean_squared_error(test["target"].values, preds, squared=False)
    r2 = r2_score(test["target"].values, preds)

    # Save last model and scaler (ensemble models not all saved to keep simple)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    plot_results(test, preds, PLOT_PATH)

    print(f"Model saved to: {os.path.abspath(MODEL_PATH)}")
    print(f"Scaler saved to: {os.path.abspath(SCALER_PATH)}")
    print(f"Plot saved to: {os.path.abspath(PLOT_PATH)}")
    print(f"Evaluation on test set: MAE={mae:.4f}, RMSE={rmse:.4f}, R2={r2:.4f}")

    display_close_col = next((c for c in df.columns if "close" in c.lower()), "Close")
    out = test[[display_close_col]].copy()
    out["Actual_next_close"] = test["target"]
    out["Predicted_next_close"] = preds
    print(out.tail(5))


if __name__ == "__main__":
    main()

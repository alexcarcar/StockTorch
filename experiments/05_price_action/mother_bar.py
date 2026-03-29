import pandas as pd
import yfinance as yf
import mplfinance as mpf

# ---------------------------------------------------------
# 1. Download OHLC data
# ---------------------------------------------------------
ticker = "AAPL"

df = yf.download(
    ticker,
    period="6mo",
    interval="1d",
    auto_adjust=False
)

# Fix MultiIndex columns and duplicates
df.columns = df.columns.get_level_values(0)
df = df.loc[:, ~df.columns.duplicated()]
df.columns = df.columns.astype(str)

# Keep only required columns
df = df[["Open", "High", "Low", "Close", "Volume"]]

# Force all columns to be numeric 1‑D Series
df = df.apply(pd.to_numeric, errors="coerce")

# ---------------------------------------------------------
# 2. Detect Mother Bar + Inside Bar pattern
# ---------------------------------------------------------
inside_indices = []
mother_indices = []

for i in range(1, len(df)):
    high_m = float(df.at[df.index[i-1], "High"])
    low_m  = float(df.at[df.index[i-1], "Low"])
    high_i = float(df.at[df.index[i], "High"])
    low_i  = float(df.at[df.index[i], "Low"])

    if (high_i < high_m) and (low_i > low_m):
        mother_indices.append(df.index[i-1])
        inside_indices.append(df.index[i])

# ---------------------------------------------------------
# 3. Highlight inside bars
# ---------------------------------------------------------
apds = []

if inside_indices:
    inside_series = pd.Series(index=df.index, dtype=float)
    inside_series.loc[inside_indices] = df.loc[inside_indices, "Close"]

    apds.append(
        mpf.make_addplot(
            inside_series,
            type="scatter",
            marker="^",
            markersize=80,
            color="orange"
        )
    )

# ---------------------------------------------------------
# 4. Shade mother bars
# ---------------------------------------------------------
vlines = [(idx, idx) for idx in mother_indices]

# ---------------------------------------------------------
# 5. Plot chart
# ---------------------------------------------------------
mpf.plot(
    df,
    type="candle",
    style="yahoo",
    title=f"{ticker} – Mother Bar / Inside Bar Pattern",
    addplot=apds,
    vlines=dict(vlines=vlines, linewidths=1, alpha=0.4, colors="purple"),
    volume=True,
    figsize=(12, 6)
)

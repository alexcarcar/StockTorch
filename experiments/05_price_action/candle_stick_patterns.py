import pandas as pd
import mplfinance as mpf

# ---------------------------------------------------------
# Helper function to plot a single pattern
# ---------------------------------------------------------
def plot_pattern(df, title):
    mpf.plot(
        df,
        type='candle',
        style='charles',
        title=title,
        ylabel='Price',
        figsize=(6, 4)
    )

# ---------------------------------------------------------
# 1. Bullish Engulfing Pattern
# ---------------------------------------------------------
# Day 1: small red candle
# Day 2: large green candle that engulfs previous body
engulfing_data = {
    'Open':  [100,  98],
    'High':  [102, 110],
    'Low':   [ 95,  97],
    'Close': [ 98, 108]
}
engulfing_df = pd.DataFrame(engulfing_data, index=pd.date_range("2024-01-01", periods=2))

plot_pattern(engulfing_df, "Bullish Engulfing Pattern")

# ---------------------------------------------------------
# 2. Doji Pattern
# ---------------------------------------------------------
# Open ≈ Close → indecision candle
doji_data = {
    'Open':  [100, 100],
    'High':  [105, 104],
    'Low':   [ 95,  96],
    'Close': [100.2, 99.8]  # nearly equal to open
}
doji_df = pd.DataFrame(doji_data, index=pd.date_range("2024-01-03", periods=2))

plot_pattern(doji_df, "Doji Candlestick Pattern")

# ---------------------------------------------------------
# 3. Momentum Candle
# ---------------------------------------------------------
# Large candle with strong directional movement
momentum_data = {
    'Open':  [100, 110],
    'High':  [103, 130],
    'Low':   [ 99, 109],
    'Close': [102, 128]  # big bullish momentum
}
momentum_df = pd.DataFrame(momentum_data, index=pd.date_range("2024-01-05", periods=2))

plot_pattern(momentum_df, "Momentum Candle Pattern")

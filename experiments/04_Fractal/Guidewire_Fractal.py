import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
from sklearn.linear_model import LinearRegression
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# -----------------------------
# USER SETTINGS
# -----------------------------
ticker = "GWRE"  # Change to your preferred ticker
start_date = "2023-06-01"
end_date = "2025-11-09"

# -----------------------------
# DOWNLOAD DATA
# -----------------------------
data = yf.download(ticker, start=start_date, end=end_date)

# Compute moving averages
data['MA20'] = data['Close'].rolling(window=20).mean()
data['MA50'] = data['Close'].rolling(window=50).mean()

# -----------------------------
# FRACTAL DETECTION
# -----------------------------
def find_fractals(df):
    bullish = []
    bearish = []
    highs = df['High'].values
    lows = df['Low'].values
    for i in range(2, len(df)-2):
        # Bearish fractal: middle high is highest among 5 bars
        if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]:
            bearish.append(i)
        # Bullish fractal: middle low is lowest among 5 bars
        if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]:
            bullish.append(i)
    return bullish, bearish

bullish_fractals, bearish_fractals = find_fractals(data)

# -----------------------------
# FRACTAL DIMENSION CALCULATION
# -----------------------------
prices = data['Close'].dropna().values
x = np.linspace(0, 1, len(prices))
y = (prices - prices.min()) / (prices.max() - prices.min())

def box_count(x, y, box_sizes):
    counts = []
    for size in box_sizes:
        nx = int(1 / size) + 1
        ny = int(1 / size) + 1
        grid = np.zeros((nx, ny), dtype=bool)
        for xi, yi in zip(x, y):
            i = int(float(xi) / size)
            j = int(float(yi) / size)
            grid[i, j] = True
        counts.append(np.sum(grid))
    return counts

box_sizes = [1/(2**k) for k in range(1, 8)]
counts = box_count(x, y, box_sizes)
log_sizes = np.log(1/np.array(box_sizes)).reshape(-1, 1)
log_counts = np.log(counts)
model = LinearRegression()
model.fit(log_sizes, log_counts)
fractal_dimension = model.coef_[0]

# -----------------------------
# PLOT CHART
# -----------------------------
fig, ax = plt.subplots(figsize=(14, 8))
dates = data.index

# Candlesticks
for i in range(len(data)):
    open_price = float(data['Open'].iloc[i])
    close_price = float(data['Close'].iloc[i])
    high_price = float(data['High'].iloc[i])
    low_price = float(data['Low'].iloc[i])
    color = 'green' if close_price >= open_price else 'red'

    # Wick
    ax.plot([dates[i], dates[i]], [low_price, high_price], color='black')

    # Body
    ax.add_patch(plt.Rectangle((dates[i], min(open_price, close_price)),
                               width=pd.Timedelta(days=0.5),
                               height=abs(close_price - open_price),
                               color=color))

# Moving averages
ax.plot(dates, data['MA20'], label='MA20', color='blue', linewidth=1.5)
ax.plot(dates, data['MA50'], label='MA50', color='orange', linewidth=1.5)

# Fractals
for i in bullish_fractals:
    ax.scatter(dates[i], data['Low'].iloc[i], marker='v', color='green', s=100, label='Bullish Fractal' if i == bullish_fractals[0] else "")
for i in bearish_fractals:
    ax.scatter(dates[i], data['High'].iloc[i], marker='^', color='red', s=100, label='Bearish Fractal' if i == bearish_fractals[0] else "")

# Formatting
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.set_title(f"{ticker} Candlestick Chart with Fractals and MAs\nFractal Dimension: {fractal_dimension:.2f}", fontsize=16)
ax.set_ylabel("Price")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
plt.savefig("candlestick_fractals.png")
plt.show()

print(f"Fractal Dimension for {ticker} from {start_date} to {end_date}: {fractal_dimension:.2f}")

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def zen_ai_signals(df, ma_length=20, use_ema=True,
                   ibs_bull_min=65.0, ibs_bear_max=35.0,
                   abr_lookback=8):
    # Moving Average
    if use_ema:
        df['ma'] = df['Close'].ewm(span=ma_length, adjust=False).mean()
    else:
        df['ma'] = df['Close'].rolling(ma_length).mean()

    # Bar ranges
    df['bar_range'] = df['High'] - df['Low']
    df['avg_range'] = df['bar_range'].rolling(abr_lookback).mean()

    # IBS calculation
    df['ibs'] = ((df['Close'] - df['Low']) / df['bar_range'] * 100).where(df['bar_range'] != 0, 50)

    # Bull/Bear conditions
    df['is_bull'] = df['Close'] > df['Open']
    df['is_bear'] = df['Close'] < df['Open']
    df['prior_bull'] = df['Close'].shift(1) > df['Open'].shift(1)
    df['prior_bear'] = df['Close'].shift(1) < df['Open'].shift(1)

    # Relation to MA
    df['bull_above_ma_now'] = df['Close'] > df['ma']
    df['bull_above_ma_prev'] = df['Close'].shift(1) > df['ma']
    df['bear_below_ma_now'] = df['Close'] < df['ma']
    df['bear_below_ma_prev'] = df['Close'].shift(1) < df['ma']

    # IBS filters
    df['bull_ibs_ok'] = (df['ibs'] > ibs_bull_min) & (df['ibs'].shift(1) > ibs_bull_min)
    df['bear_ibs_ok'] = (df['ibs'] < ibs_bear_max) & (df['ibs'].shift(1) < ibs_bear_max)

    # Range filter
    df['range_ok'] = (df['bar_range'] > df['avg_range']) | (df['bar_range'].shift(1) > df['avg_range'])

    # Signals
    df['bull_signal'] = (df['is_bull'] & df['prior_bull'] &
                         df['bull_above_ma_now'] & df['bull_above_ma_prev'] &
                         df['bull_ibs_ok'] & df['range_ok'])

    df['bear_signal'] = (df['is_bear'] & df['prior_bear'] &
                         df['bear_below_ma_now'] & df['bear_below_ma_prev'] &
                         df['bear_ibs_ok'] & df['range_ok'])

    return df

# ✅ Fetch data from Yahoo Finance
ticker = 'AAPL'
data = yf.download(ticker, period='3mo', interval='1d', group_by='ticker')

# ✅ Flatten columns if multi-index
data.columns = [col[1] if isinstance(col, tuple) else col for col in data.columns]

# ✅ Apply Zen AI logic
signals_df = zen_ai_signals(data)

# ✅ Plot candlestick chart using Matplotlib
fig, ax = plt.subplots(figsize=(12, 6))

# Convert dates for plotting
signals_df['Date'] = mdates.date2num(signals_df.index)

# Candlestick bars
for idx, row in signals_df.iterrows():
    color = 'green' if row['Close'] >= row['Open'] else 'red'
    ax.plot([row['Date'], row['Date']], [row['Low'], row['High']], color='black')  # Wick
    ax.add_patch(plt.Rectangle((row['Date'] - 0.2, min(row['Open'], row['Close'])),
                               0.4, abs(row['Close'] - row['Open']),
                               color=color))  # Body

# Plot MA line
ax.plot(signals_df['Date'], signals_df['ma'], color='yellow', label='MA')

# Plot bull signals (green arrows)
bull_dates = signals_df['Date'][signals_df['bull_signal']]
bull_prices = signals_df['Low'][signals_df['bull_signal']]
ax.scatter(bull_dates, bull_prices, marker='^', color='green', s=100, label='Bull Signal')

# Plot bear signals (red arrows)
bear_dates = signals_df['Date'][signals_df['bear_signal']]
bear_prices = signals_df['High'][signals_df['bear_signal']]
ax.scatter(bear_dates, bear_prices, marker='v', color='red', s=100, label='Bear Signal')

# Format chart
ax.xaxis_date()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)
plt.title(f'{ticker} Price with Zen AI Signals')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

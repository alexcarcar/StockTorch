import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf

# Generate some sample data
dates = pd.date_range('2023-01-01', periods=30)
data = pd.DataFrame(index=dates)
data['Open'] = [100 + i for i in range(30)]
data['High'] = data['Open'] + 10
data['Low'] = data['Open'] - 10
data['Close'] = data['Open'] + 5

# Plot the candlestick graph
mpf.plot(data, type='candle', style='charles', title='Candlestick Graph', ylabel='Price (USD)')

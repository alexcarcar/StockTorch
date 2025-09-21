import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# Download NVDA stock data for the last 30 days
ticker = 'NVDA'
data = yf.download(ticker, period='30d')

# Calculate the moving average
window_size = 5
data['Moving_Avg'] = data['Close'].rolling(window=window_size).mean()

# Plot the data and the moving average
plt.figure(figsize=(10, 6))
plt.plot(data['Close'], label='NVDA Close Price')
plt.plot(data['Moving_Avg'], label='Moving Average', color='orange')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title('NVDA Stock Price and Moving Average')
plt.legend()
plt.show()
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# Download NVDA stock data for the last 30 days
ticker = input("Ticker symbol? ")
ticker = ticker.upper()
# ticker = 'NVDA'

days = int(input("How many past days do you want to look at? "))
days = str(days) + "d"
window_size = int(input("What moving average size? "))
window_size2 = int(input("What moving average2 size? "))

data = yf.download(ticker, period=days)
# Calculate the moving average
# window_size = 5
data['Moving_Avg'] = data['Close'].rolling(window=window_size).mean()
data['Moving_Avg2'] = data['Close'].rolling(window=window_size2).mean()

# Plot the data and the moving average
plt.figure(figsize=(10, 6))
plt.plot(data['Close'], label=ticker + ' Close Price')
plt.plot(data['Moving_Avg'], label='Moving Average (' + str(window_size) +')', color='orange')
plt.plot(data['Moving_Avg2'], label='Moving Average ('+ str(window_size2) +')', color='yellow')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.title(ticker + ' Stock Price and Moving Average')
plt.legend()
plt.show()

# print(data)
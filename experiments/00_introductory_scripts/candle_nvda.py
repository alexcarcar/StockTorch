import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import yfinance as yf

# Download NVDA stock data for the last 90 days
ticker = 'NVDA'
stock = yf.Ticker(ticker)
data = stock.history(period='30d')

# Plot the candlestick graph
mpf.plot(data, type='candle', style='charles', title='NVDA Candlestick Graph', ylabel='Price (USD)')
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import yfinance as yf

# Download stock data for the last n days
ticker = input('Enter ticker symbol: ').upper()
stock = yf.Ticker(ticker)
n = int(input('Enter number of days: '))
days = str(n)+'d'
data = stock.history(period=days)

# Plot the candlestick graph
mpf.plot(data, type='candle', style='charles', title=ticker + ' Candlestick Graph', ylabel='Price (USD)')
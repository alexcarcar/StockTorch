import mplfinance as mpf
import pandas as pd
import yfinance as yf

df = yf.download('MESZ25.CME', interval='1d', auto_adjust=True)

# Ensure DataFrame is not empty and columns are valid
if not df.empty:
    ohlc_cols = [col for col in ['Open', 'High', 'Low', 'Close'] if col in df.columns]
    for col in ohlc_cols + (['Volume'] if 'Volume' in df.columns else []):
        df[col] = pd.to_numeric(df[col], errors='coerce')

    if ohlc_cols:
        df = df.dropna(subset=ohlc_cols)

        for span, name, color in [(200, 'EMA_200', 'blue'), (20, 'EMA_20', 'orange'), (10, 'EMA_10', 'green')]:
            df[name] = df[ohlc_cols[-1]].ewm(span=span, adjust=False).mean()

        addplots = [mpf.make_addplot(df[name], color=color, width=1.2)
                    for name, color in zip(['EMA_200', 'EMA_20', 'EMA_10'], ['blue', 'orange', 'green'])]

        mpf.plot(
            df,
            type='candle',
            style='charles',
            addplot=addplots,
            title='MESZ 2025 Candlestick with 200, 20, 10 EMA',
            ylabel='Price',
            volume='Volume' in df.columns
        )
    else:
        print("Required OHLC columns not found in downloaded data.")
else:
    print("No data downloaded. Check the ticker symbol or data availability.")

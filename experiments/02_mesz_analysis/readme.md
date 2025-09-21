# Experiment: 02_mesz_analysis
# MESZ Candlestick Analysis with EMAs

This experiment visualizes daily candlestick data for the MESZ25 futures contract using Python. It downloads historical price data, calculates exponential moving averages (EMAs), and plots the results with volume.

## Overview

- Downloads MESZ25.CME daily price data from Yahoo Finance
- Calculates 200, 20, and 10-day EMAs on closing prices
- Plots candlestick chart with EMAs and volume using mplfinance

## Requirements

- Python 3.8+
- pandas
- yfinance
- mplfinance

Install dependencies:

```bash
pip install pandas yfinance mplfinance
```

## Usage

1. Run the script:

    ```bash
    python mesz.py
    ```

2. The script will display a candlestick chart with 200, 20, and 10-day EMAs and volume (if available).

## File Structure

- Downloads and cleans OHLCV data
- Calculates EMAs
- Plots candlestick chart with overlays

---

Feel free to modify the script to analyze other tickers or adjust EMA spans.

# Experiment 01: PyTorch Analysis
# Stock Pattern Recognition with PyTorch

This experiment demonstrates how to use a PyTorch LSTM model to recognize patterns in historical stock price data and predict future closing prices.

## Overview

- Loads historical stock data from a CSV file
- Prepares time series sequences for model training
- Defines an LSTM-based neural network for regression
- Trains the model to predict the next closing price based on previous prices

## Requirements

- Python 3.8+
- PyTorch
- pandas

Install dependencies:

```bash
pip install torch pandas
```

## Usage

1. Prepare your stock data in a CSV file named `historical_stock_data.csv` with a `Close` column.
2. Run the script:

```bash
python stock_pattern_recognition.py
```

The script will train an LSTM model for 10 epochs and print the training loss for each epoch.

## File Structure

- `StockDataset`: Loads and prepares time series data from CSV
- `StockLSTM`: LSTM-based regression model
- `train_model`: Training loop for the model

---

Feel free to modify the script or experiment with different model architectures and parameters.

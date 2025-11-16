import yfinance as yf
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Download historical stock data (example: Apple)
ticker = "AAPL"
data = yf.download(ticker, start="2020-01-01", end="2023-01-01")

# 2. Create simple features
data["Return"] = data["Close"].pct_change()
data["MA5"] = data["Close"].rolling(5).mean()
data["MA10"] = data["Close"].rolling(10).mean()

# 3. Define target: 1 if next day return > 0, else 0
data["Target"] = (data["Return"].shift(-1) > 0).astype(int)

# Drop NaN values
data = data.dropna()

# 4. Prepare features and labels
X = data[["Return", "MA5", "MA10"]]
y = data["Target"]

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 6. Train a simple model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7. Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# 8. Example prediction for the last day
last_features = X.iloc[-1].values.reshape(1, -1)
prediction = model.predict(last_features)
print(f"Predicted next-day movement for {ticker}: {'Up' if prediction[0] == 1 else 'Down'}")

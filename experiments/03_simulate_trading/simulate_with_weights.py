import random
import matplotlib.pyplot as plt

class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.history = [price]

    def simulate_day(self):
        change_percent = random.uniform(-0.05, 0.05)
        self.price *= (1 + change_percent)
        self.history.append(self.price)

class Portfolio:
    def __init__(self, cash, stock_list):
        self.cash = cash
        self.holdings = {stock.name: 0 for stock in stock_list}

    def buy(self, stock, amount):
        cost = stock.price * amount
        if self.cash >= cost:
            self.cash -= cost
            self.holdings[stock.name] += amount

    def sell(self, stock, amount):
        if self.holdings.get(stock.name, 0) >= amount:
            self.holdings[stock.name] -= amount
            revenue = stock.price * amount
            self.cash += revenue

    def value(self, stock_list):
        total = self.cash
        for stock in stock_list:
            total += self.holdings.get(stock.name, 0) * stock.price
        return total

def simulate_trading():
    # Initialize stocks
    apple = Stock("AAPL", 150)
    google = Stock("GOOGL", 2800)
    stocks = [apple, google]

    # Simulate 30 days of price movement
    for _ in range(30):
        for stock in stocks:
            stock.simulate_day()

    # Initialize portfolios
    initial_cash = 10000
    portfolio1 = Portfolio(initial_cash, stocks)  # Buy on drop
    portfolio2 = Portfolio(initial_cash, stocks)  # Buy on rise
    value1 = []
    value2 = []

    scaling_factor = 200  # Controls trade aggressiveness

    # Apply strategies
    for day in range(1, 31):
        for stock in stocks:
            yesterday = stock.history[day - 1]
            today = stock.history[day]
            change_percent = (today - yesterday) / yesterday
            trade_amount = int(abs(change_percent) * scaling_factor)

            # Strategy 1: Buy on drop, sell on rise
            if change_percent < 0:
                portfolio1.buy(stock, trade_amount)
            elif change_percent > 0:
                portfolio1.sell(stock, trade_amount)

            # Strategy 2: Buy on rise, sell on drop
            if change_percent > 0:
                portfolio2.buy(stock, trade_amount)
            elif change_percent < 0:
                portfolio2.sell(stock, trade_amount)

        value1.append(portfolio1.value(stocks))
        value2.append(portfolio2.value(stocks))

    # Plot stock prices
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    for stock in stocks:
        plt.plot(stock.history, label=stock.name)
    plt.title("Stock Price Simulation")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()

    # Combined profit comparison
    plt.subplot(1, 2, 2)
    plt.plot([v - initial_cash for v in value1], label="Buy on Drop", color='blue')
    plt.plot([v - initial_cash for v in value2], label="Buy on Rise", color='green')
    plt.title("Profit Comparison (Weighted Strategy)")
    plt.xlabel("Days")
    plt.ylabel("Profit ($)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

simulate_trading()

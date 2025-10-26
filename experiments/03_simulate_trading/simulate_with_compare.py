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
    def __init__(self, cash):
        self.cash = cash
        self.holdings = {}

    def buy(self, stock, amount):
        cost = stock.price * amount
        if self.cash >= cost:
            self.cash -= cost
            self.holdings[stock.name] = self.holdings.get(stock.name, 0) + amount

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
    # Simulate stock prices once
    apple = Stock("AAPL", 150)
    google = Stock("GOOGL", 2800)
    stocks = [apple, google]

    for _ in range(30):
        for stock in stocks:
            stock.simulate_day()

    # Strategy 1: Buy on drop, sell on rise
    portfolio1 = Portfolio(10000)
    value1 = []

    # Strategy 2: Buy on rise, sell on drop
    portfolio2 = Portfolio(10000)
    value2 = []

    for day in range(1, 31):
        for stock in stocks:
            # Strategy 1
            if stock.history[day] < stock.history[day - 1]:
                portfolio1.buy(stock, 1)
            elif stock.history[day] > stock.history[day - 1]:
                portfolio1.sell(stock, 1)

            # Strategy 2
            if stock.history[day] > stock.history[day - 1]:
                portfolio2.buy(stock, 1)
            elif stock.history[day] < stock.history[day - 1]:
                portfolio2.sell(stock, 1)

        value1.append(portfolio1.value(stocks))
        value2.append(portfolio2.value(stocks))

    # Plot results
    plt.figure(figsize=(12, 6))

    # Stock prices
    plt.subplot(1, 3, 1)
    for stock in stocks:
        plt.plot(stock.history, label=stock.name)
    plt.title("Stock Price Simulation")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()

    # Strategy 1 profit
    plt.subplot(1, 3, 2)
    plt.plot([v - 10000 for v in value1], label="Buy on Drop", color='blue')
    plt.title("Profit: Buy on Drop")
    plt.xlabel("Days")
    plt.ylabel("Profit ($)")
    plt.legend()

    # Strategy 2 profit
    plt.subplot(1, 3, 3)
    plt.plot([v - 10000 for v in value2], label="Buy on Rise", color='green')
    plt.title("Profit: Buy on Rise")
    plt.xlabel("Days")
    plt.ylabel("Profit ($)")
    plt.legend()

    plt.tight_layout()
    plt.show()

simulate_trading()

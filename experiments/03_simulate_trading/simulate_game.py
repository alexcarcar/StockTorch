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
            print(f"Bought {amount} shares of {stock.name} at ${stock.price:.2f}")
        else:
            print("Not enough cash to buy.")

    def sell(self, stock, amount):
        if self.holdings.get(stock.name, 0) >= amount:
            self.holdings[stock.name] -= amount
            revenue = stock.price * amount
            self.cash += revenue
            print(f"Sold {amount} shares of {stock.name} at ${stock.price:.2f}")
        else:
            print("Not enough shares to sell.")

    def value(self, stock_list):
        total = self.cash
        for stock in stock_list:
            total += self.holdings.get(stock.name, 0) * stock.price
        return total

def simulate_trading():
    apple = Stock("AAPL", 150)
    google = Stock("GOOGL", 2800)
    stocks = [apple, google]
    portfolio = Portfolio(10000)

    for day in range(30):
        print(f"\nDay {day + 1}")
        for stock in stocks:
            stock.simulate_day()
            print(f"{stock.name}: ${stock.price:.2f}")

        # Simple strategy: buy if price dropped, sell if it rose
        for stock in stocks:
            if len(stock.history) > 1:
                if stock.price < stock.history[-2]:
                    portfolio.buy(stock, 1)
                elif stock.price > stock.history[-2]:
                    portfolio.sell(stock, 1)

        print(f"Portfolio value: ${portfolio.value(stocks):.2f}")

    # Plot stock prices
    for stock in stocks:
        plt.plot(stock.history, label=stock.name)
    plt.title("Stock Price Simulation")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plt.show()

simulate_trading()

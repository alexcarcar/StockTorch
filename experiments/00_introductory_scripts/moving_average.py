import matplotlib.pyplot as plt
import numpy as np

# Generate some sample data
np.random.seed(0)
data = np.random.randn(100).cumsum()

# Calculate the moving average
window_size = 5
moving_avg = np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Plot the data and the moving average
plt.figure(figsize=(10, 6))
plt.plot(data, label='Original Data')
plt.plot(range(window_size - 1, len(data)), moving_avg, label='Moving Average', color='orange')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Moving Average')
plt.legend()
plt.show()

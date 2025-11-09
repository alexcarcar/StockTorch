import matplotlib.pyplot as plt
import numpy as np


# Recursive function to draw a tree fractal
def draw_tree(x, y, length, angle, depth, branch_angle, shrink_factor):
    if depth == 0:
        return

    # Calculate the end point of the branch
    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)

    # Draw the branch
    plt.plot([x, x_end], [y, y_end], color='brown', linewidth=depth)

    # Recursively draw the left and right branches
    draw_tree(x_end, y_end, length * shrink_factor, angle + branch_angle, depth - 1, branch_angle, shrink_factor)
    draw_tree(x_end, y_end, length * shrink_factor, angle - branch_angle, depth - 1, branch_angle, shrink_factor)


# Set up the plot
plt.figure(figsize=(8, 8))
plt.axis('off')

# Initial parameters for the tree
start_x = 0
start_y = 0
initial_length = 100
initial_angle = np.pi / 2  # pointing upwards
depth = 10
branch_angle = np.pi / 6  # 30 degrees
shrink_factor = 0.7

# Draw the tree fractal
draw_tree(start_x, start_y, initial_length, initial_angle, depth, branch_angle, shrink_factor)

# Adjust plot limits
plt.xlim(-150, 150)
plt.ylim(0, 200)

# Show the fractal tree
plt.show()
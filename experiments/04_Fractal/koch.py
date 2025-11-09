import matplotlib.pyplot as plt
import numpy as np

def koch_snowflake(order, scale=10):
    def initial_triangle(scale):
        p1 = np.array([0, 0])
        p2 = np.array([scale, 0])
        p3 = np.array([scale/2, scale*np.sqrt(3)/2])
        return [p1, p2, p3, p1]

    def koch_iteration(points):
        new_points = []
        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            delta = p2 - p1
            one_third = p1 + delta / 3
            two_third = p1 + 2 * delta / 3
            angle = np.pi / 3
            rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                        [np.sin(angle), np.cos(angle)]])
            peak = one_third + rotation_matrix.dot(delta / 3)
            new_points += [p1, one_third, peak, two_third]
        new_points.append(points[-1])
        return new_points

    points = initial_triangle(scale)
    for _ in range(order):
        points = koch_iteration(points)
    return np.array(points)

# Parameters
order = 4  # Increase for more detail
scale = 10

snowflake_points = koch_snowflake(order, scale)

plt.figure(figsize=(8, 8))
plt.axis('equal')
plt.axis('off')
plt.plot(snowflake_points[:, 0], snowflake_points[:, 1], color='blue')
plt.title(f'Koch Snowflake (Order {order})')
plt.show()
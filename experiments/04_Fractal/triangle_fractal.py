import matplotlib.pyplot as plt
import numpy as np


def sierpinski_triangle(vertices, depth):
    if depth == 0:
        triangle = plt.Polygon(vertices, edgecolor='black', facecolor='white')
        plt.gca().add_patch(triangle)
    else:
        mid01 = ((vertices[0][0] + vertices[1][0]) / 2, (vertices[0][1] + vertices[1][1]) / 2)
        mid12 = ((vertices[1][0] + vertices[2][0]) / 2, (vertices[1][1] + vertices[2][1]) / 2)
        mid20 = ((vertices[2][0] + vertices[0][0]) / 2, (vertices[2][1] + vertices[0][1]) / 2)

        sierpinski_triangle([vertices[0], mid01, mid20], depth - 1)
        sierpinski_triangle([vertices[1], mid12, mid01], depth - 1)
        sierpinski_triangle([vertices[2], mid20, mid12], depth - 1)


plt.figure(figsize=(8, 8))
plt.axis('equal')
plt.axis('off')

vertices = [(0, 0), (1, 0), (0.5, np.sqrt(3) / 2)]
depth = 6  # Adjust for more or less detail

sierpinski_triangle(vertices, depth)
plt.show()
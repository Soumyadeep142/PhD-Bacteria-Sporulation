import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
import pandas as pd

# Function to define the circle residuals
def calc_R(xc, yc, x, y):
    return np.sqrt((x - xc)**2 + (y - yc)**2)

def residuals(c, x, y):
    Ri = calc_R(c[0], c[1], x, y)
    return Ri - Ri.mean()

# Circle fitting function
def fit_circle(x, y):
    x = np.array(x)
    y = np.array(y)
    x_m = np.mean(x)
    y_m = np.mean(y)
    
    result = least_squares(residuals, x0=[x_m, y_m], args=(x, y))
    xc, yc = result.x
    Ri = calc_R(xc, yc, x, y)
    R = Ri.mean()
    
    return xc, yc, R

# Example usage:
# Replace these with your (x, y) points

df = pd.read_csv('time_0.csv')

x_points = df['X'].tolist()
y_points = df['Y'].tolist()

xc, yc, R = fit_circle(x_points, y_points)
print(f"Center: ({xc:.3f}, {yc:.3f})")
print(f"Radius: {R:.3f}")

# Optional: plot the points and the fitted circle
theta = np.linspace(0, 2 * np.pi, 100)
x_fit = xc + R * np.cos(theta)
y_fit = yc + R * np.sin(theta)

plt.figure()
plt.plot(x_points, y_points, 'ro', label='Data Points')
plt.plot(x_fit, y_fit, 'b-', label='Fitted Circle')
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.title('Circle Fit to Points')
plt.grid()
plt.show()


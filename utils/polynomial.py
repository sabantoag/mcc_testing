import matplotlib.pyplot as plt
import numpy as np
from typing import List


CALIBRATED_COEFFICIENTS = [-2.3475136, 4.6729021, -7.24486402, 4.98339161]  # x^n + x^(n-1) + ... + x^0

def create_polynomial(coefficients: List[float]) -> np.poly1d:
    """Creates a polynomial from the given coefficients.

    Args:
        coefficients (List[float]): List of coefficients for the polynomial, starting from the highest degree.

    Returns:
        np.poly1d: Polynomial returned as a numpy poly1d object.
    """
    polynomial = np.poly1d(coefficients)
    return polynomial


def plot_polynomial(polynomial: np.poly1d, x_range: tuple[float, float], num_points: int = 1000):
    """Plots the polynomial over a specified range.

    Args:
        polynomial (np.poly1d): The polynomial to plot.
        x_range (tuple[float, float]): The range of x values to plot the polynomial over.
        num_points (int): Number of points to use for plotting.
    """
    x_values = np.linspace(x_range[0], x_range[1], num_points)
    y_values = polynomial(x_values)

    plt.plot(x_values, y_values, label=str(polynomial))
    plt.title('Polynomial Plot')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid()
    plt.legend()
    plt.show()

import numpy as np
from typing import List


def create_polynomial(coefficients: List[float]) -> np.poly1d:
    """Creates a polynomial from the given coefficients.

    Args:
        coefficients (List[float]): List of coefficients for the polynomial, starting from the highest degree.

    Returns:
        np.poly1d: Polynomial returned as a numpy poly1d object.
    """
    polynomial = np.poly1d(coefficients)
    return polynomial

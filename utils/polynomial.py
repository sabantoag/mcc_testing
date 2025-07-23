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

import numpy as np

CALIBRATED_COEFFICIENTS = [-5.9441039, 1.40338961, 0.28746753, 4.94402715]  # x^n + x^(n-1) + ... + x^0

def create_polynomial(coefficients: list[int | float]) -> np.poly1d:
    """Creates a polynomial from the given coefficients.

    Args:
        coefficients (list[int  |  float]): List of coefficients for the polynomial, starting from the highest degree.

    Returns:
        np.poly1d: Polynomial returned as a numpy poly1d object.
    """
    polynomial = np.poly1d(coefficients)
    return polynomial

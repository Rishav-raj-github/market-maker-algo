import numpy as np

def calculate_ewma(data: np.ndarray, alpha: float) -> np.ndarray:
    """
    Calculates Exponentially Weighted Moving Average.
    Optimized for NumPy arrays.
    """
    ewma = np.zeros_like(data)
    ewma[0] = data[0]
    for i in range(1, len(data)):
        ewma[i] = alpha * data[i] + (1 - alpha) * ewma[i-1]
    return ewma

def calculate_volatility(prices: np.ndarray, window: int = 20) -> float:
    """
    Calculates annualized volatility from price arrays.
    """
    if len(prices) < 2:
        return 0.0
    returns = np.diff(prices) / prices[:-1]
    # Simple standard deviation scaled by sqrt of assumed ticks in a year
    return np.std(returns) * np.sqrt(252 * 25200)

def normalize_price(price: float, tick_size: float) -> float:
    """Rounds a price to the nearest tick size increment."""
    return round(round(price / tick_size) * tick_size, 8)

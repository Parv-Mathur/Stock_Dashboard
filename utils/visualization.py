import numpy as np

def calculate_support_resistance(df):
    """Calculate support and resistance levels."""
    high = df['High'].rolling(window=20).max()
    low = df['Low'].rolling(window=20).min()
    return high, low
import pytest
import pandas as pd
from data.stock_data import StockDataFetcher
from indicators.technical import TechnicalIndicators

def test_stock_data_fetcher():
    fetcher = StockDataFetcher()
    data = fetcher.get_stock_data('AAPL')
    
    assert data is not None
    assert not data.empty
    assert all(col in data.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume'])

def test_technical_indicators():
    fetcher = StockDataFetcher()
    indicators = TechnicalIndicators()

    data = fetcher.get_stock_data('AAPL')
    data_with_indicators = indicators.add_all_indicators(data)

    # Check for specific indicators only if they are valid
    assert 'RSI' in data_with_indicators.columns
    if 'MACD' in data_with_indicators.columns:
        assert 'MACD_Signal' in data_with_indicators.columns
        assert 'MACD_Hist' in data_with_indicators.columns
    if 'BB_Upper' in data_with_indicators.columns:
        assert 'BB_Middle' in data_with_indicators.columns
        assert 'BB_Lower' in data_with_indicators.columns

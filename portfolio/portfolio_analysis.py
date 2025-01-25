import pandas as pd
import numpy as np
from typing import List
from data.stock_data import StockDataFetcher

class PortfolioAnalysis:
    def __init__(self, stocks: List[str]):
        self.stocks = stocks
        self.fetcher = StockDataFetcher()
        
    def fetch_portfolio_data(self, period='1y'):
        portfolio_data = {}
        for stock in self.stocks:
            data = self.fetcher.get_stock_data(stock, period)
            portfolio_data[stock] = data['Close']
        return pd.DataFrame(portfolio_data)
    
    def calculate_portfolio_returns(self, weights=None):
        data = self.fetch_portfolio_data()
        
        # Normalize data
        normalized_data = data / data.iloc[0]
        
        # Default equal weights if not provided
        if weights is None:
            weights = [1/len(self.stocks)] * len(self.stocks)
        
        # Calculate weighted portfolio returns
        portfolio_returns = normalized_data.mul(weights).sum(axis=1)
        
        return portfolio_returns
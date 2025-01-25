import yfinance as yf
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataFetcher:
    def __init__(self):
        self.cache = {}
        
    def get_stock_data(self, symbol: str, period: str = '1mo', interval: str = '1d'):
        try:
            cache_key = f"{symbol}_{period}_{interval}"
            
            if cache_key in self.cache:
                logger.info(f"Returning cached data for {symbol}")
                return self.cache[cache_key]
            
            logger.info(f"Fetching new data for {symbol}")
            stock = yf.Ticker(symbol)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                logger.error(f"No data received for {symbol}")
                return None
                
            df = self._preprocess_data(df)
            self.cache[cache_key] = df
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
            
    def _preprocess_data(self, df):
        df = df.dropna()
        df.index = pd.to_datetime(df.index)
        return df

# Test the implementation
if __name__ == "__main__":
    fetcher = StockDataFetcher()
    data = fetcher.get_stock_data('AAPL')
    print(data.head())
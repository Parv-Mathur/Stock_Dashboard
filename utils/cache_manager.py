import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json

class CacheManager:
    def __init__(self, db_path='cache.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS stock_cache
            (symbol TEXT, period TEXT, interval TEXT,
             data TEXT, timestamp DATETIME,
             PRIMARY KEY (symbol, period, interval))
        ''')
        conn.commit()
        conn.close()
    
    def get_cached_data(self, symbol, period, interval):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT data, timestamp FROM stock_cache
            WHERE symbol=? AND period=? AND interval=?
        ''', (symbol, period, interval))
        result = c.fetchone()
        conn.close()
        
        if result:
            data, timestamp = result
            timestamp = datetime.fromisoformat(timestamp)
            
            # Check if cache is still valid (15 min for intraday, 24h for daily)
            if interval.endswith('m'):
                valid_duration = timedelta(minutes=15)
            else:
                valid_duration = timedelta(hours=24)
                
            if datetime.now() - timestamp <= valid_duration:
                return pd.read_json(data)
        return None
    
    def cache_data(self, symbol, period, interval, data):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO stock_cache
            (symbol, period, interval, data, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            symbol,
            period,
            interval,
            data.to_json(),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
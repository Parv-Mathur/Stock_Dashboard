from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd

class TrendPredictor:
    def __init__(self, data):
        self.data = data
        self.model = None
    
    def prepare_features(self):
        # Create lagged features
        features = self.data.copy()
        features['Close_Prev_1'] = features['Close'].shift(1)
        features['Close_Prev_2'] = features['Close'].shift(2)
        features['Close_Prev_3'] = features['Close'].shift(3)
        
        # Drop NaN rows
        features.dropna(inplace=True)
        
        return features
    
    def train_model(self):
        features = self.prepare_features()
        
        X = features[['Close_Prev_1', 'Close_Prev_2', 'Close_Prev_3']]
        y = features['Close']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        self.model = RandomForestRegressor(n_estimators=100)
        self.model.fit(X_train_scaled, y_train)
        
        return self.model
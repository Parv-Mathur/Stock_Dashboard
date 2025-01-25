import pandas as pd
import numpy as np

class TechnicalSignals:
    @staticmethod
    def get_rsi_signals(df, overbought=70, oversold=30):
        """Generate RSI-based trading signals"""
        signals = pd.DataFrame(index=df.index)
        signals['RSI_Signal'] = 0
        
        # Oversold signal (potential buy)
        signals.loc[df['RSI'] < oversold, 'RSI_Signal'] = 1
        
        # Overbought signal (potential sell)
        signals.loc[df['RSI'] > overbought, 'RSI_Signal'] = -1
        
        return signals
    
    @staticmethod
    def get_macd_signals(df):
        """Generate MACD-based trading signals"""
        signals = pd.DataFrame(index=df.index)
        signals['MACD_Signal'] = 0
        
        # Buy signal: MACD crosses above signal line
        signals.loc[
            (df['MACD'] > df['MACD_Signal']) &
            (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1)),
            'MACD_Signal'
        ] = 1
        
        # Sell signal: MACD crosses below signal line
        signals.loc[
            (df['MACD'] < df['MACD_Signal']) &
            (df['MACD'].shift(1) >= df['MACD_Signal'].shift(1)),
            'MACD_Signal'
        ] = -1
        
        return signals
    
    @staticmethod
    def get_bb_signals(df):
        """Generate Bollinger Bands-based signals"""
        signals = pd.DataFrame(index=df.index)
        signals['BB_Signal'] = 0
        
        # Price below lower band (potential buy)
        signals.loc[df['Close'] < df['BB_Lower'], 'BB_Signal'] = 1
        
        # Price above upper band (potential sell)
        signals.loc[df['Close'] > df['BB_Upper'], 'BB_Signal'] = -1
        
        return signals
    
    def get_combined_signals(self, df):
        """Combine all technical signals"""
        rsi_signals = self.get_rsi_signals(df)
        macd_signals = self.get_macd_signals(df)
        bb_signals = self.get_bb_signals(df)
        
        combined = pd.DataFrame(index=df.index)
        combined['Signal'] = (
            rsi_signals['RSI_Signal'] +
            macd_signals['MACD_Signal'] +
            bb_signals['BB_Signal']
        )
        
        return combined
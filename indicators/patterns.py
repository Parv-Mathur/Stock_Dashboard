import pandas_ta as ta

class PatternRecognition:
    @staticmethod
    def detect_patterns(df):
        # Add Bullish Engulfing Pattern
        df['Bullish_Engulfing'] = ta.cdl_pattern(
            open_=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='cdl_engulfing'
        )
        # Add Bearish Harami Pattern
        df['Bearish_Harami'] = ta.cdl_pattern(
            open_=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='cdl_harami'
        )
        return df

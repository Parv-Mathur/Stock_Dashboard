import pandas_ta as ta

class TechnicalIndicators:
    @staticmethod
    def add_moving_averages(df):
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['EMA_20'] = ta.ema(df['Close'], length=20)
        return df

    @staticmethod
    def add_rsi(df, period=14):
        df['RSI'] = ta.rsi(df['Close'], length=period)
        return df

    @staticmethod
    def add_macd(df):
        macd = ta.macd(df['Close'])
        if macd is not None:
            df['MACD'] = macd['MACD_12_26_9']
            df['MACD_Signal'] = macd['MACDs_12_26_9']
            df['MACD_Hist'] = macd['MACDh_12_26_9']
        return df

    @staticmethod
    def add_bollinger_bands(df, period=20):
        bb = ta.bbands(df['Close'], length=period)
        if bb is not None:
            df['BB_Upper'] = bb['BBU_20_2.0']
            df['BB_Middle'] = bb['BBM_20_2.0']
            df['BB_Lower'] = bb['BBL_20_2.0']
        return df

    def add_all_indicators(self, df):
        df = self.add_moving_averages(df)
        df = self.add_rsi(df)
        df = self.add_macd(df)  # Ensure MACD columns are added
        df = self.add_bollinger_bands(df)  # Ensure BB columns are added
        return df

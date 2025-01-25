import pandas as pd
import numpy as np

class PerformanceMetrics:
    @staticmethod
    def calculate_returns(df):
        """Calculate various return metrics"""
        metrics = {}
        
        # Daily returns
        daily_returns = df['Close'].pct_change()
        
        # Basic metrics
        metrics['Total Return'] = (
            (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
        )
        metrics['Annualized Return'] = (
            ((1 + metrics['Total Return']/100) ** (252/len(df)) - 1) * 100
        )
        metrics['Daily Volatility'] = daily_returns.std() * 100
        metrics['Annualized Volatility'] = metrics['Daily Volatility'] * np.sqrt(252)
        
        # Risk metrics
        metrics['Sharpe Ratio'] = (
            np.sqrt(252) * daily_returns.mean() / daily_returns.std()
        )
        metrics['Max Drawdown'] = (
            (df['Close'] / df['Close'].cummax() - 1).min() * 100
        )
        
        # Format metrics
        return {k: f"{v:.2f}%" if k != 'Sharpe Ratio' else f"{v:.2f}"
                for k, v in metrics.items()}
    
    @staticmethod
    def calculate_signal_performance(df, signals):
        """Calculate performance metrics for trading signals"""
        performance = pd.DataFrame(index=df.index)
        
        # Calculate returns based on signals
        performance['Signal'] = signals['Signal']
        performance['Returns'] = df['Close'].pct_change()
        performance['Strategy Returns'] = (
            performance['Signal'].shift(1) * performance['Returns']
        )
        
        # Calculate cumulative returns
        performance['Cumulative Returns'] = (1 + performance['Returns']).cumprod()
        performance['Strategy Cumulative Returns'] = (
            1 + performance['Strategy Returns']
        ).cumprod()
        
        return performance
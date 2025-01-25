import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data.stock_data import StockDataFetcher
from indicators.technical import TechnicalIndicators
from utils.watchlist import Watchlist
from utils.visualization import calculate_support_resistance
from indicators.patterns import PatternRecognition

@st.cache_data
def get_cached_data(symbol, period, interval):
    fetcher = StockDataFetcher()
    return fetcher.get_stock_data(symbol, period, interval)

def create_chart(data, indicators_enabled):
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Price', 'Volume', 'Indicators'),
        row_heights=[0.5, 0.2, 0.3]
    )
    # Main price chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    # Bollinger Bands
    if indicators_enabled.get('BB', False):
        for band, color in [('BB_Upper', 'rgba(0,128,0,0.3)'),
                            ('BB_Middle', 'rgba(0,128,0,0.7)'),
                            ('BB_Lower', 'rgba(0,128,0,0.3)')]:
            if band in data.columns:
                fig.add_trace(
                    go.Scatter(x=data.index, y=data[band], name=band, line=dict(color=color)),
                    row=1, col=1
                )
    # Volume chart
    fig.add_trace(
        go.Bar(x=data.index, y=data['Volume'], name='Volume'),
        row=2, col=1
    )
    # Support/Resistance
    support, resistance = calculate_support_resistance(data)
    if support is not None and resistance is not None:
        fig.add_trace(go.Scatter(x=data.index, y=support, name='Support', line=dict(color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=resistance, name='Resistance', line=dict(color='red')), row=1, col=1)
    # RSI
    if indicators_enabled.get('RSI', False) and 'RSI' in data.columns:
        fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'), row=3, col=1)
    # MACD
    if indicators_enabled.get('MACD', False) and {'MACD', 'MACD_Signal'}.issubset(data.columns):
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD'), row=3, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal'), row=3, col=1)
    fig.update_layout(height=1000, showlegend=True, xaxis_rangeslider_visible=False)
    return fig

def main():
    st.set_page_config(page_title="Stock Analysis", layout="wide")
    st.title("Stock Market Technical Analysis Dashboard")
    symbol = st.sidebar.text_input("Stock Symbol", value="AAPL")
    period = st.sidebar.selectbox("Time Period", ['1mo', '3mo', '6mo', '1y'], index=0)
    indicators_enabled = {
        'BB': st.sidebar.checkbox('Bollinger Bands', value=True),
        'RSI': st.sidebar.checkbox('RSI', value=True),
        'MACD': st.sidebar.checkbox('MACD', value=True)
    }
    data = get_cached_data(symbol, period, '1d')
    if data is not None and not data.empty:
        indicators = TechnicalIndicators()
        data = indicators.add_all_indicators(data)
        data = PatternRecognition.detect_patterns(data)
        fig = create_chart(data, indicators_enabled)
        st.plotly_chart(fig, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${data['Close'].iloc[-1]:.2f}")
        col2.metric("RSI", f"{data['RSI'].iloc[-1]:.1f}")
        col3.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
    else:
        st.error("No data available. Check the stock symbol or timeframe.")

if __name__ == "__main__":
    main()

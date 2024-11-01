import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

def fetch_stock_data(tickers, lookback_days):
    """Fetch historical stock data."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=lookback_days)
    
    try:
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        if data.empty:
            raise ValueError("No data retrieved from Yahoo Finance")
        return data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        raise

def calculate_portfolio_metrics(daily_returns):
    """Calculate expected returns and covariance matrix."""
    expected_returns = daily_returns.mean() * 252  # Annualized returns
    cov_matrix = daily_returns.cov() * 252  # Annualized covariance
    return expected_returns, cov_matrix

def portfolio_performance(weights, expected_returns, cov_matrix):
    """Calculate portfolio performance metrics."""
    if not np.isclose(np.sum(weights), 1.0):
        weights = weights / np.sum(weights)  # Normalize weights
    
    portfolio_return = np.sum(weights * expected_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility != 0 else 0
    
    return portfolio_return, portfolio_volatility, sharpe_ratio

def create_portfolio_performance_plot(data, weights):
    """Create a plot showing individual stock and portfolio performance."""
    # Normalize stock prices to start at 100
    normalized_data = data / data.iloc[0] * 100
    
    # Create traces for each stock
    traces = [
        go.Scatter(
            x=normalized_data.index, 
            y=normalized_data[ticker], 
            name=f'{ticker} Performance',
            mode='lines'
        ) for ticker in normalized_data.columns
    ]
    
    # Calculate weighted portfolio performance
    portfolio_performance = normalized_data.mul(weights).sum(axis=1)
    traces.append(
        go.Scatter(
            x=portfolio_performance.index, 
            y=portfolio_performance, 
            name='Portfolio Performance', 
            line=dict(color='black', width=3),
            mode='lines'
        )
    )
    
    # Layout
    layout = go.Layout(
        title='Asset and Portfolio Performance',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Normalized Performance (Base 100)'),
        template='plotly_white'
    )
    
    # Create figure
    fig = go.Figure(data=traces, layout=layout)
    return fig
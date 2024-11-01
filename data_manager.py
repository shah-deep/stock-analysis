import yfinance as yf

def fetch_stock_data(tickers, start_date, end_date):
    """Fetch historical stock data for given tickers between start_date and end_date."""
    try:
        data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        if data.empty:
            raise ValueError("No data retrieved from Yahoo Finance")
        return data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        raise

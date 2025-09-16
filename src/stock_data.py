import yfinance as yf
import json
from functools import lru_cache
import re

@lru_cache(maxsize=50)
def get_stock_data_by_period(ticker: str, time_period: str) -> str:
    """
    Fetch stock data for a given time period (like "1d", "1mo", "1y").
    
    Args:
        ticker: The ticker symbol of the stock.
        time_period: The time period to get the stock data for. 
                      (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, ytd, max)
    
    Returns:
        A JSON string containing stock data for the given time period, or error JSON.
    """
    if not isinstance(ticker, str) or not ticker.strip():
        return json.dumps({"error": "Invalid ticker provided."})
    
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "10y", "ytd", "max"]
    if time_period not in valid_periods:
        return json.dumps({"error": f"Invalid time period: {time_period}. Valid options: {', '.join(valid_periods)}"})
    
    try:
        data = yf.Ticker(ticker)
        stock_data = data.history(period=time_period)

        if stock_data.empty:
            return json.dumps({"error": f"No data available for ticker {ticker} with the time period {time_period}"})
        
        return stock_data.to_json(orient="records")
    except Exception as e:
        print(f"Error in get_stock_data_by_period for {ticker}: {str(e)}")
        return json.dumps({"error": f"Failed to fetch data - {str(e)}"})

@lru_cache(maxsize=50)
def get_stock_data_by_dates(ticker: str, start_date: str, end_date: str) -> str:
    """
    Fetch stock data between a specific date range.
    
    Args:
        ticker: The ticker symbol of the stock.
        start_date: The start date in 'YYYY-MM-DD' format.
        end_date: The end date in 'YYYY-MM-DD' format.
    
    Returns:
        A JSON string containing stock data for the given date range, or error JSON.
    """
    if not isinstance(ticker, str) or not ticker.strip():
        return json.dumps({"error": "Invalid ticker provided."})
    
    # Validate date format (YYYY-MM-DD)
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not (re.match(date_pattern, start_date) and re.match(date_pattern, end_date)):
        return json.dumps({"error": "Invalid date format. Use YYYY-MM-DD."})
    
    try:
        data = yf.Ticker(ticker)
        stock_data = data.history(start=start_date, end=end_date)

        if stock_data.empty:
            return json.dumps({"error": f"No data available for ticker {ticker} between {start_date} and {end_date}"})
        
        return stock_data.to_json(orient="records")
    except Exception as e:
        print(f"Error in get_stock_data_by_dates for {ticker}: {str(e)}")
        return json.dumps({"error": f"Failed to fetch data - {str(e)}"})
from mcp.server.fastmcp import FastMCP

from src.news_chain import get_news_analysis as get_news_analysis_chain
from src.stock_data import get_stock_data_by_dates, get_stock_data_by_period
from src.analyze_sentiment import get_sentiment_analysis
from src.financial_advisor import get_financial_advisor
from src.market_trend import get_market_trends

# MCP server instance
mcp = FastMCP("FinFlow")

@mcp.tool()
def get_news(stock_symbol: str) -> str:
    """
    Fetches news for a stock symbol using DuckDuckGo and returns an analysis.

    Parameters:
        stock_symbol (str): The stock symbol to find information about

    Returns:
        str: A news analysis
    """
    return get_news_analysis_chain(stock_symbol)

@mcp.tool()
def get_stock_data(stock_symbol: str, time_period: str = "1y", start_date: str = None, end_date: str = None) -> str:
    """
    Fetches stock data for a given stock symbol based on time period or date range using yfinance.

    Args:
        stock_symbol (str): The stock symbol (e.g., 'AAPL', 'GOOG') to fetch data for.
        time_period (str, optional): The time period for data. Default is "1y".
                                     Valid options are (1d, 5d, 1mo, 3mo, 6mo, 1y, 5y, 10y, ytd, max)
        start_date (str, optional): The start date for the date range in 'YYYY-MM-DD' format.
        end_date (str, optional): The end date for the date range in 'YYYY-MM-DD' format.

    Returns:
        str: A JSON string containing stock data or an error message.
    
    Example:
        get_stock_data("AAPL", time_period="1mo")
        get_stock_data("AAPL", start_date="2025-04-01", end_date="2025-04-10")
    """
    if start_date and end_date:
        return get_stock_data_by_dates(stock_symbol, start_date, end_date)
    return get_stock_data_by_period(stock_symbol, time_period)

@mcp.tool()
def analyze_sentiment(text: str) -> str:
    """
    Analyzes the sentiment of financial or stock-related text using a language model (LLM) via Ollama.

    Args:
        text (str): The financial or stock-related input text to analyze.

    Returns:
        str: A structured string containing the sentiment classification and a brief reasoning.
    """
    return get_sentiment_analysis(text)

@mcp.tool()
def track_market_trends(stock_symbol: str) -> str:
    """ 
    Tracks and provides a market trend for a given stock symbol by querying DuckDuckGo and summarizing using Ollama.
    
    Arguments:
        stock_symbol (str): The stock symbol to fetch market trends for.

    Returns:
        str: A market trend summary or error message.
    """
    return get_market_trends(stock_symbol)

@mcp.tool()
def financial_advisor(stock_symbol: str) -> str:
    """ 
    Provides financial advice based on stock symbol by fetching stock data and analyzing sentiment.
    
    Arguments:
        stock_symbol (str): The stock symbol to provide financial advice for.

    Returns:
        str: Financial advice or error message.
    """
    return get_financial_advisor(stock_symbol)

# Start the MCP server and make it ready to accept requests
if __name__ == "__main__":
    mcp.run()
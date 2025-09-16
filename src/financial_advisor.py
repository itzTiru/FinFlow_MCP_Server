from langchain_ollama import ChatOllama
from src.stock_data import get_stock_data_by_period
from src.news_chain import get_news_analysis as get_news_analysis_chain
from src.analyze_sentiment import get_sentiment_analysis
from functools import lru_cache
import json

@lru_cache(maxsize=50)
def get_financial_advisor(stock_symbol: str) -> str:
    """ 
    Provides financial advice based on stock symbol by fetching stock data and analyzing sentiment.
    
    Arguments:
        stock_symbol (str): The stock symbol to provide financial advice for.

    Returns:
        str: Financial advice or error message.
    """
    if not isinstance(stock_symbol, str) or not stock_symbol.strip():
        return "Error: Invalid stock symbol provided."

    try:
        llm = ChatOllama(
            model="llama3.2:latest",
            temperature=0.2,
        )
        stock_data = get_stock_data_by_period(stock_symbol, time_period="1mo")
        
        # Check for JSON error response
        try:
            stock_data_json = json.loads(stock_data)
            if "error" in stock_data_json:
                return f"Error: {stock_data_json['error']}"
        except json.JSONDecodeError:
            pass  # Not an error JSON, proceed with raw stock_data
        
        news_analysis = get_news_analysis_chain(stock_symbol)
        
        if "Error" in news_analysis:
            return news_analysis
        
        sentiment = get_sentiment_analysis(news_analysis)

        if "Error" in sentiment:
            return sentiment
        
        prompt = f"""
        You are a financial advisor. Based on the following data and news for the stock symbol {stock_symbol}, provide concise financial advice.
        
        Stock Data (last month): {stock_data}

        Recent News: {news_analysis}

        Recent News Sentiment: {sentiment}
        
        Your advice should consider the stock's recent performance, sentiment, and any upcoming market trends.
        """
        
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error in get_financial_advisor for {stock_symbol}: {str(e)}")
        return f"Error: Failed to generate financial advice - {str(e)}"
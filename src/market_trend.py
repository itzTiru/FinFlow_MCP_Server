from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from functools import lru_cache

@lru_cache(maxsize=50)
def get_market_trends(stock_symbol: str) -> str:
    """ 
    Tracks and provides a market trend for a given stock symbol by querying DuckDuckGo and summarizing using Ollama.
    
    Arguments:
        stock_symbol (str): The stock symbol to fetch market trends for.

    Returns:
        str: A market trend summary or error message.
    """
    if not isinstance(stock_symbol, str) or not stock_symbol.strip():
        return "Error: Invalid stock symbol provided."

    try:
        llm = ChatOllama(
            model="llama3.2:latest",
            temperature=0.2,
        )
        
        search = DuckDuckGoSearchRun()
        
        query = f"Market trend for {stock_symbol}"
        search_result = search.invoke(query)
        
        if not search_result:
            return "Error: No search results found for market trends."

        prompt = f"""
        You are a financial expert and market analyst. Here is a search query: {query}
        The following are some search results related to this market trend query:
        
        {search_result}

        Based on these search results, provide a detailed analysis of the stock's current market trend, the key drivers, and potential future outlook.
        """
        
        llm_response = llm.invoke(prompt)
        
        return llm_response.content
    except Exception as e:
        print(f"Error in get_market_trends for {stock_symbol}: {str(e)}")
        return f"Error: Failed to retrieve market trends - {str(e)}"
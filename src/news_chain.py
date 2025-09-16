from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from functools import lru_cache

@lru_cache(maxsize=50)
def get_news_analysis(query: str):
    if not isinstance(query, str) or not query.strip():
        return "Error: Invalid query provided."

    try:
        llm = ChatOllama(
            model = "llama3.2:latest",
            temperature = 0.2,
        )

        search = DuckDuckGoSearchRun()
        result = search.invoke(f"What are the latest news on {query}")

        if not result:
            return "Error: No news results found."

        llm_response = llm.invoke(f"""
You are a financial expert and news analyst. Here's a query: What are the latest news on {query}
The following are the latest articles related to the query:
{result}

Based on these articles, provide a detailed analysis of the current news trends, potential impacts, and any key takeaways.
""")
        
        return llm_response.content
    except Exception as e:
        print(f"Error in get_news_analysis for {query}: {str(e)}")
        return f"Error: Failed to retrieve news analysis - {str(e)}"
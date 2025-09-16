from langchain_ollama import ChatOllama
from functools import lru_cache

@lru_cache(maxsize=50)
def get_sentiment_analysis(text: str) -> str:
    """
    Analyzes the sentiment of the given financial or stock-related text using an LLM via Ollama.

    Args:
        text (str): The input financial/news text.

    Returns:
        str: A structured sentiment output including classification and reasoning, or error message.
    """
    if not isinstance(text, str) or not text.strip():
        return "Error: Invalid text provided."

    try:
        llm = ChatOllama(
            model="llama3.2:latest",
            temperature=0.2,
        )

        prompt = f"""
You are a financial sentiment analyst.

Analyze the sentiment of the following financial news or stock-related text and classify it as:
- Positive
- Negative
- Neutral

Also provide a one-line explanation for your sentiment classification.

Text:
{text}

Respond in the following format:
Sentiment: <Positive|Negative|Neutral>
Reason: <Short explanation>
"""

        llm_response = llm.invoke(prompt)
        return llm_response.content
    except Exception as e:
        print(f"Error in get_sentiment_analysis: {str(e)}")
        return f"Error: Failed to analyze sentiment - {str(e)}"
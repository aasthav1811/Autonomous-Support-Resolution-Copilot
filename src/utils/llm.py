from langchain_ollama import ChatOllama
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def get_llm(temperature: float = 0.0):
    """
    Returns a local Ollama LLM — completely free, no API key needed.
    Make sure Ollama is running: `ollama serve`
    And the model is pulled: `ollama pull llama3.2`
    """
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
    )

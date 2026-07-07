from src.config import (
    LLM_PROVIDER,
    GROQ_MODEL,
    ANTHROPIC_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)


def get_llm(temperature: float = 0.0):
    """
    Returns the chat model for the configured provider.

    - LLM_PROVIDER=groq (default): Groq cloud, free tier. Requires GROQ_API_KEY.
    - LLM_PROVIDER=anthropic: Claude API. Requires ANTHROPIC_API_KEY.
      Note: current Claude models (Opus 4.7+) reject sampling params like
      temperature, so the argument is ignored on this provider.
    - LLM_PROVIDER=ollama: local Ollama — free, no API key.
      Make sure Ollama is running (`ollama serve`) and the model is pulled.
    """
    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=temperature,
        )

    if LLM_PROVIDER == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
        )

    from langchain_groq import ChatGroq

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature,
        max_tokens=1024,
    )

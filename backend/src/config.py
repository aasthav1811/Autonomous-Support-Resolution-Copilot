import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider: "groq" (hosted, free tier — default), "anthropic" (Claude
# API), or "ollama" (local, free — requires `ollama serve` running)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

# Groq (hosted, free tier — https://console.groq.com/keys)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Anthropic (Claude API)
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-8")

# Ollama (local dev only)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Embeddings: ChromaDB's built-in ONNX all-MiniLM-L6-v2 (no PyTorch needed)
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "support_kb"

# Comma-separated list of origins allowed to call the API from a browser
CORS_ORIGINS = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if o.strip()
]

CATEGORIES = ["billing", "technical", "account", "shipping", "general"]
URGENCY_LEVELS = ["low", "medium", "high", "critical"]

TEAM_ROUTING = {
    "billing": "Finance Team",
    "technical": "Engineering Team",
    "account": "Account Management",
    "shipping": "Logistics Team",
    "general": "Tier 1 Support",
}

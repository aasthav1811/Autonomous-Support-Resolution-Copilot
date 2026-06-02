import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Free local embedding model (no API needed)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "support_kb"

CATEGORIES = ["billing", "technical", "account", "shipping", "general"]
URGENCY_LEVELS = ["low", "medium", "high", "critical"]

TEAM_ROUTING = {
    "billing": "Finance Team",
    "technical": "Engineering Team",
    "account": "Account Management",
    "shipping": "Logistics Team",
    "general": "Tier 1 Support",
}

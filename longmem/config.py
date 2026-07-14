"""LongMem configuration, loaded from environment / .env file."""
import os

from dotenv import load_dotenv

load_dotenv()

# --- PostgreSQL ---
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_NAME = os.getenv("PG_NAME", "longmem")
PG_USER = os.getenv("PG_USER", "maxkb")
PG_PASSWORD = os.getenv("PG_PASSWORD", "MaxKb#2026pg")

# --- Embedding backend ---
# provider: "openai" (any OpenAI-compatible endpoint) | "fallback" (local, no API key)
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "fallback")
EMBED_BASE_URL = os.getenv("EMBED_BASE_URL", "https://api.openai.com/v1")
EMBED_API_KEY = os.getenv("EMBED_API_KEY", "")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
# Must match the actual embedding dimension. 384 for fallback, 1536 for text-embedding-3-small.
EMBED_DIM = int(os.getenv("EMBED_DIM", "384"))

# --- Optional LLM summarization ---
SUMMARY_ENABLED = os.getenv("SUMMARY_ENABLED", "false").lower() == "true"
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# --- Defaults ---
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "5"))
DEFAULT_THRESHOLD = float(os.getenv("DEFAULT_THRESHOLD", "0.0"))

# --- Service ---
SERVICE_HOST = os.getenv("SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "8123"))

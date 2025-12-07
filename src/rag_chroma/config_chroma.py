import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base path = root of your project
BASE_DIR = Path(__file__).resolve().parents[3]

# Read PDF folder from .env (your env says ../data/raw_data)
PDF_FOLDER = os.getenv("PDF_FOLDER", "../data/raw_data")
RAW_PDF_DIR = (BASE_DIR / PDF_FOLDER).resolve()

# Correct FOLDER NAMES based on your screenshot
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed_data"
VECTOR_DB_DIR = DATA_DIR / "vector_database"

# Create directories if missing
RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# From your .env
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL", "gpt-4.1-mini")

# Chroma collection name
CHROMA_COLLECTION_NAME = "foleys_docs"

DEFAULT_TOP_K = 5

# rag_chroma/retrieval_chroma/retriever_chroma.py

import chromadb
from chromadb.utils import embedding_functions

from ..utils_chroma.config_chroma import (
    VECTOR_DB_DIR,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    OPENAI_API_KEY,
    DEFAULT_TOP_K,
)
from ..utils_chroma.logging_utils_chroma import get_logger

logger = get_logger(__name__)


def get_relevant_chunks(query: str, k: int = DEFAULT_TOP_K):
    """Retrieve top-k relevant text chunks from ChromaDB."""

    logger.info(f"Connecting to Chroma at: {VECTOR_DB_DIR}")

    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

    embedder = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL_NAME,
    )

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=embedder,
    )

    logger.info(f"Running semantic search for query: {query}")

    results = collection.query(
        query_texts=[query],
        n_results=k,
    )

    # Results come as list-of-lists → we unwrap them
    return {
        "ids": results.get("ids", [[]])[0],
        "documents": results.get("documents", [[]])[0],
        "metadatas": results.get("metadatas", [[]])[0],
        "distances": results.get("distances", [[]])[0],
    }

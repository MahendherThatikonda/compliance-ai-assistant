# rag_chroma/generation_chroma/rag_pipeline_chroma.py

from ..retrieval_chroma.retriever_chroma import get_relevant_chunks
from .llm_client_chroma import call_llm
from ..utils_chroma.logging_utils_chroma import get_logger

logger = get_logger(__name__)


def build_prompt(query: str, contexts: list[str]) -> list[dict]:
    """Build a prompt that injects retrieved context into the conversation."""

    context_block = "\n\n---\n\n".join(contexts)

    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful assistant. You MUST answer ONLY using the provided "
            "context. If information is missing, say 'I don't know'."
        )
    }

    user_msg = {
        "role": "user",
        "content": (
            f"Context:\n{context_block}\n\n"
            f"Question: {query}\n\n"
            "Use ONLY the above context in your answer."
        )
    }

    return [system_msg, user_msg]


def answer_query(query: str, k: int = 5):
    """Perform full RAG pipeline: retrieve → build prompt → LLM answer."""
    results = get_relevant_chunks(query, k)

    contexts = results["documents"]
    metadata = results["metadatas"]

    if not contexts:
        logger.warning("No relevant contexts retrieved.")
        return {
            "answer": "I couldn't find relevant information in the knowledge base.",
            "sources": [],
        }

    messages = build_prompt(query, contexts)
    answer = call_llm(messages)

    return {
        "answer": answer,
        "sources": metadata,
    }


if __name__ == "__main__":
    test = answer_query("What does the handbook say about safety rules?")
    print("\nANSWER:\n", test["answer"])
    print("\nSOURCES:\n", test["sources"])

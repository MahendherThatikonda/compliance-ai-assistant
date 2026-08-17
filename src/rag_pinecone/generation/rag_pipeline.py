from ..retrieval.retriever import retrieve
from .llm_client import generate

def rag_answer(query):
    matches = retrieve(query)
    context = "\n\n".join(m.metadata["text"] for m in matches)

    system = "Answer only using provided context. If unknown, say 'Not enough information'."
    user = f"Question: {query}\n\nContext:\n{context}"

    answer = generate(system, user)

    sources = []

    for m in matches:
        source = m.metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return {
        "answer": answer,
        "sources": sources
    }
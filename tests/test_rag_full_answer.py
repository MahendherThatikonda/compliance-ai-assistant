from openai import OpenAI
from src.rag_pinecone.retrieval import retrieve
from src.rag_pinecone.config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)


def build_context(matches, max_chars: int = 6000) -> str:
    parts = []
    total = 0

    for m in matches:
        md = m.metadata or {}
        text = md.get("text", "")
        source = md.get("source", "unknown document")
        year = md.get("year", "unknown year")
        standard_code = md.get("standard_code", "")

        header = f"[{standard_code} {year} — {source}]"
        chunk = f"{header}\n{text.strip()}\n"

        if total + len(chunk) > max_chars:
            break

        parts.append(chunk)
        total += len(chunk)

    return "\n\n".join(parts)


def answer_question(question: str, k: int = 5) -> str:
    matches = retrieve(question)[:k]
    context = build_context(matches)

    prompt = f"""
You are a plumbing and drainage standards assistant.

Use ONLY the information in the Context below to answer the Question.
Do NOT invent requirements that are not supported by the context.

- Summarise the requirements in clear, simple language.
- Focus on practical rules that a plumber / designer needs to follow.
- Include citations like ({{standard_code}} {{year}}, {{source}}).
- If the answer is not clearly stated, say the context does not provide enough detail.

Question:
{question}

Context:
{context}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",   # <--- FIXED: USING A REAL MODEL NAME
        messages=[{"role": "user", "content": prompt}],
    )

    return resp.choices[0].message.content


if __name__ == "__main__":
    q="According to AS/NZS 3500.4:2003, what are the requirements for heated water relief valves?"
#    q = "For a typical residential house, what are the requirements for gully traps under AS/NZS 3500.2?"
    print("QUESTION:", q)
    print("\nANSWER:\n")
    print(answer_question(q))

import sys, os
sys.path.append(os.path.abspath("."))
from src.rag_pinecone.retrieval.retriever import retrieve


def test(question):
    print(f"\nQUESTION: {question}")
    matches = retrieve(question)
    print(f"Number of matches: {len(matches)}")

    if not matches:
        print("No matching documents found.")
        return

    for m in matches[:5]:  # show top 5
        md = m.metadata
        print(
            f"- source={md.get('source')}, "
            f"code={md.get('standard_code')}, "
            f"year={md.get('year')}, "
            f"is_latest={md.get('is_latest')}"
        )


# ---------------- RUN TESTS ---------------- #

test("According to AS/NZS 3500.2:2021, what are the rules for vents?")

test("previous version of AS/NZS 3500.2 for wet vent requirements")
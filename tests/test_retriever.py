import sys, os
sys.path.append(os.path.abspath("."))
from src.rag_pinecone.retrieval.retriever import retrieve


def test(question):
    print(f"\nQUESTION: {question}")
    matches = retrieve(question)

    for m in matches[:5]:  # show top 5
        md = m.metadata
        print(
            f"- source={md.get('source')}, "
            f"code={md.get('standard_code')}, "
            f"year={md.get('year')}, "
            f"is_latest={md.get('is_latest')}"
        )


# ---------------- RUN TESTS ---------------- #

test("What are the requirements for gully traps?")

test("According to AS/NZS 3500.2:2015, what are the rules for vents?")

test("previous version of AS/NZS 3500.4 for heated water services")

test("3500.2 2003 wet vent requirements")

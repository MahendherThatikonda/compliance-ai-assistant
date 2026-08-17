import re
from pinecone import Pinecone
from openai import OpenAI
from ..config import *
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def embed_query(q):
    r = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[q],
        dimensions=EMBEDDING_DIM
    )
    return r.data[0].embedding

# ---------- NEW: build metadata filter based on the question ---------- #

def _normalise_standard_code(raw: str) -> str | None:
    """
    Turn something like:
      'AS 3500.2', 'AS/NZS3500.2', '3500.2'
    into:
      'AS/NZS 3500.2'
    so it matches what you stored as `standard_code` in metadata.
    """
    series_match = re.search(r"3500(?:\.\d+)?", raw)
    if not series_match:
        return None
    series_key = series_match.group(0)  # e.g. '3500.2'
    return f"AS/NZS {series_key}"

def build_metadata_filter(question: str) -> dict:
    """
    Decide which version of the standards to use based on how the user asks.

    Rules:
    - Default: only latest versions -> is_latest == True
    - If user mentions AS/NZS 3500.x + specific year -> filter by that year
    - If user says 'previous version of AS/NZS 3500.x' -> is_latest == False
    """
    q = question.lower()

    # 1) Pattern: 'AS/NZS 3500.2:2015' or 'AS 3500.2 2015'
#    m = re.search(r"(as\/?nzs?\s*3500(?:\.\d+)?)\D*(19|20)\d{2}", q, re.IGNORECASE)
    m = re.search(
    r"(as\/?nzs?\s*3500(?:\.\d+)?)\D*((?:19|20)\d{2})",
    q,
    re.IGNORECASE,
    )
    if m:
        raw_code = m.group(1)
        year_str = m.group(2)
        standard_code = _normalise_standard_code(raw_code)
        if standard_code:
            year = int(year_str)
            return {
                "standard_code": {"$eq": standard_code},
                "year": {"$eq": year},
            }

    # 2) Pattern: mentions AS/NZS 3500.x and 'previous / older / old version'
    has_prev_word = any(
        phrase in q
        for phrase in ["previous version", "older version", "old version", "earlier version"]
    )
    code_only = re.search(r"(as\/?nzs?\s*3500(?:\.\d+)?)", q, re.IGNORECASE)

    if has_prev_word and code_only:
        raw_code = code_only.group(1)
        standard_code = _normalise_standard_code(raw_code)
        if standard_code:
            return {
                "standard_code": {"$eq": standard_code},
                "is_latest": {"$eq": False},
            }

    # 3) (Optional) If user mentions a year and a standard without 'AS/NZS' prefix
    #    e.g. "3500.2 2015 gully trap requirements"
    loose_code = re.search(r"3500(?:\.\d+)?", q)
    loose_year = re.search(r"(19|20)\d{2}", q)
    if loose_code and loose_year:
        standard_code = _normalise_standard_code(loose_code.group(0))
        year = int(loose_year.group(0))
        if standard_code:
            return {
                "standard_code": {"$eq": standard_code},
                "year": {"$eq": year},
            }

    # 4) Default: only latest versions of all standards
    return {
        "is_latest": {"$eq": True}
    }
'''
def retrieve(q):
    logger.info("Searching knowledge base...")
    # Decide which version(s) to search
    meta_filter = build_metadata_filter(q)
    res = index.query(vector=embed_query(q), top_k=TOP_K, include_metadata=True,filter=meta_filter)
    return res.matches'''

def retrieve(q):
    logger.info("Searching knowledge base...")

    meta_filter = build_metadata_filter(q)

    print("FILTER:", meta_filter)

    res = index.query(
        vector=embed_query(q),
        top_k=TOP_K,
        include_metadata=True,
        filter=meta_filter,
    )

    return res.matches
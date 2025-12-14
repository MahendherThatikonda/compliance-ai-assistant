import re
from pinecone import Pinecone
from openai import OpenAI
from ..config import *
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def embed_query(q: str):
    r = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[q],
        dimensions=EMBEDDING_DIM,
    )
    return r.data[0].embedding


# ---------- Metadata filter helpers ---------- #

def _normalise_standard_code(raw: str) -> str | None:
    """
    Extract the 3500 series from the raw text and normalise to what we
    stored in metadata as `standard_code`.

    Examples of `raw`:
        'AS 3500.2', 'AS/NZS3500.2', '3500.4', 'as nzs 3500'
    We return:
        'AS/NZS 3500'
    """
    if re.search(r"3500", raw):
        return "AS/NZS 3500"
    return None


def build_metadata_filter(question: str) -> dict:
    """
    Build a Pinecone metadata filter from the natural-language question.

    Rules:
    - Default: only latest versions -> is_latest == True
    - If user mentions AS/NZS 3500.x + specific year -> filter by that year
    - If user says 'previous / older / old / earlier version of AS/NZS 3500.x'
      -> filter by that code with is_latest == False
    """

    q = question.lower()

    # ---- 1) Explicit code + year, e.g.
    # "According to AS/NZS 3500.2:2015 ..." or "AS 3500.4 2003 ..."
    code_year_match = re.search(
        r"(as\/?nzs?\s*3500(?:\.\d+)?)\D*((?:19|20)\d{2})",
        q,
        re.IGNORECASE,
    )

    if code_year_match:
        raw_code = code_year_match.group(1)
        year_str = code_year_match.group(2)
        standard_code = _normalise_standard_code(raw_code)

        if standard_code:
            year = int(year_str)
            meta = {
                "standard_code": {"$eq": standard_code},
                "year": {"$eq": year},
            }
            logger.info(f"Using explicit code+year filter: {meta}")
            return meta

    # ---- 2) "previous/older/earlier/old version of AS/NZS 3500.x ..."
    has_prev_word = any(
        phrase in q
        for phrase in [
            "previous version",
            "older version",
            "old version",
            "earlier version",
        ]
    )
    code_only_match = re.search(r"(as\/?nzs?\s*3500(?:\.\d+)?)", q, re.IGNORECASE)

    if has_prev_word and code_only_match:
        raw_code = code_only_match.group(1)
        standard_code = _normalise_standard_code(raw_code)
        if standard_code:
            meta = {
                "standard_code": {"$eq": standard_code},
                "is_latest": {"$eq": False},
            }
            logger.info(f"Using 'previous version' filter: {meta}")
            return meta

    # ---- 3) Loose pattern: "3500.2 2003 wet vent requirements"
    loose_code = re.search(r"3500(?:\.\d+)?", q)
    loose_year = re.search(r"((?:19|20)\d{2})", q)
    if loose_code and loose_year:
        standard_code = _normalise_standard_code(loose_code.group(0))
        if standard_code:
            year = int(loose_year.group(1))
            meta = {
                "standard_code": {"$eq": standard_code},
                "year": {"$eq": year},
            }
            logger.info(f"Using loose code+year filter: {meta}")
            return meta

    # ---- 4) Default: only latest versions
    meta = {"is_latest": {"$eq": True}}
    logger.info(f"Using default 'latest only' filter: {meta}")
    return meta


def retrieve(q: str):
    logger.info("Searching knowledge base...")
    meta_filter = build_metadata_filter(q)
    logger.info(f"Metadata filter for '{q}': {meta_filter}")

    res = index.query(
        vector=embed_query(q),
        top_k=TOP_K,
        include_metadata=True,
        filter=meta_filter,
    )

    matches = res.matches
    logger.info(f"Matches returned: {len(matches)}")
    for i, m in enumerate(matches, start=1):
        md = m.metadata or {}
        logger.info(
            f"[{i}] source={md.get('source')}, "
            f"standard_code={md.get('standard_code')}, "
            f"year={md.get('year')}, "
            f"is_latest={md.get('is_latest')}"
        )

    return matches

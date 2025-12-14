import uuid
import re

import os
from collections import defaultdict

from tqdm import tqdm
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

from ..config import *
from ..utils.logging_utils import get_logger
from .pdf_loader import list_pdfs, extract_text_from_pdf
from .text_splitter import simple_char_chunk

logger = get_logger(__name__)

# Ensure required env vars are present (loaded via config.py / .env).
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set. Add it to your .env file.")
if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY is not set. Add it to your .env file.")
if not PINECONE_INDEX_NAME:
    raise RuntimeError("PINECONE_INDEX_NAME is not set. Add it to your .env file.")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)


def get_index():
    existing = [i["name"] for i in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing:
        logger.info(f"Creating Pinecone index: {PINECONE_INDEX_NAME}")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric="cosine",
            cloud="aws",
            region="us-east-1",
            embed={"model": EMBEDDING_MODEL, "field_map": {"text": "chunk_text"}},
        )

    logger.info(f"Using index: {PINECONE_INDEX_NAME}")
    return pc.Index(PINECONE_INDEX_NAME)


def embed_batch(texts):
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL, input=texts, dimensions=EMBEDDING_DIM
    )
    return [item.embedding for item in response.data]


def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text for better embedding.
    """

    # Remove page numbers like "Page 1", "page 12"
    text = re.sub(r"Page\s*\d+", " ", text, flags=re.IGNORECASE)

    # Remove multiple newlines
    text = re.sub(r"\n+", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove hyphenation line breaks: "build-\ning" -> "building"
    text = re.sub(r"-\s+", "", text)

    # Normalize unicode quotes/dashes
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")

    return text.strip()

# -------------------- NEW: parse standard + year from filename -------------------- #

def parse_standard_metadata(file_path: str) -> dict:
    """
    Extracts series_key (e.g. '3500.2') and year (e.g. 2018) from the PDF filename.

    Adjust the regexes below to match your actual filenames if needed, e.g.
    'ASNZS_3500.2_2018.pdf' or 'AS NZS 3500.2-2018 Plumbing and drainage.pdf'
    """
    filename = os.path.basename(file_path)

    # find '3500' or '3500.2'
    series_match = re.search(r"3500(?:\.\d+)?", filename)
    series_key = series_match.group(0) if series_match else None

    # find a 4-digit year
    year_match = re.search(r"(19|20)\d{2}", filename)
    year = int(year_match.group(0)) if year_match else None

    # nice label – tweak if your standards are not all AS/NZS 3500.x
    standard_code = f"AS/NZS {series_key}" if series_key else None

    return {
        "file": file_path,
        "filename": filename,
        "series_key": series_key,
        "year": year,
        "standard_code": standard_code,
    }

def build_index_from_pdfs():
    index = get_index()
    pdfs = list_pdfs()

  # 1) First pass: work out latest year for each series_key
    file_meta_list = [parse_standard_metadata(f) for f in pdfs]

    latest_by_series = defaultdict(int)
    for meta in file_meta_list:
        if meta["series_key"] and meta["year"]:
            latest_by_series[meta["series_key"]] = max(
                latest_by_series[meta["series_key"]],
                meta["year"],
            )

    # 2) Second pass: index chunks and attach metadata
    for meta in file_meta_list:
        file = meta["file"]
        series_key = meta["series_key"]
        year = meta["year"]
        standard_code = meta["standard_code"]

        is_latest = (
            series_key is not None
            and year is not None
            and year == latest_by_series.get(series_key)
        )

        base_metadata = {
            "source": meta["filename"],   # original file name
            "standard_code": standard_code,
            "series_key": series_key,
            "year": year,
            "is_latest": is_latest,       # 👈 this powers "latest only" queries
        }
   # Drop any fields that are None so Pinecone doesn't see null values
        base_metadata = {k: v for k, v in base_metadata.items() if v is not None}

        raw_text = extract_text_from_pdf(file)
        text = clean_text(raw_text)
        chunks = simple_char_chunk(text)

        for i in tqdm(range(0, len(chunks), 50), desc=f"Indexing {meta['filename']}"):
            batch = chunks[i : i + 50]
            embeddings = embed_batch(batch)

            vectors = [
                {
                    "id": str(uuid.uuid4()),
                    "values": emb,
                    "metadata": {
                        **base_metadata,
                        "text": chunk,   # keep chunk text
                    },
                }
                for emb, chunk in zip(embeddings, batch)
            ]

            index.upsert(vectors)
    logger.info("Vector DB Build Complete")

if __name__ == "__main__":
    logger.info("Starting PDF indexing pipeline...")
    build_index_from_pdfs()
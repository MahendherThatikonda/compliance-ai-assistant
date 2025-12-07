import uuid
import re
from tqdm import tqdm
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

from ..config import *
from ..utils.logging_utils import get_logger
from .pdf_loader import list_pdfs, extract_text_from_pdf
from .text_splitter import simple_char_chunk

logger = get_logger(__name__)

PINECONE_API_KEY='pcsk_2pD8bn_EPmnhaD75GbJ2pKu9E6GLybFUAeFQW4trzkjXFCzVNtajktwtGXFsdyGEzE5Sdu'

PINECONE_INDEX_NAME='foleys-rag-index'

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
            embed={
            "model":EMBEDDING_MODEL,
            "field_map":{"text": "chunk_text"}
            }
        )


    logger.info(f"Using index: {PINECONE_INDEX_NAME}")
    return pc.Index(PINECONE_INDEX_NAME)


def embed_batch(texts):
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
        dimensions=EMBEDDING_DIM
    )
    return [item.embedding for item in response.data]


def clean_text(text: str) -> str:
    """
    Cleans extracted PDF text for better embedding.
    """

    # Remove page numbers like "Page 1", "page 12"
    text = re.sub(r'Page\s*\d+',' ', text, flags=re.IGNORECASE)

    # Remove multiple newlines
    text = re.sub(r'\n+', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove hyphenation line breaks: "build-\ning" → "building"
    text = re.sub(r'-\s+', '', text)

    # Normalize unicode quotes/dashes
    text = text.replace("–","-").replace("—","-").replace("’","'")

    return text.strip()


def build_index_from_pdfs():
    index = get_index()
    pdfs = list_pdfs()

    for file in pdfs:
        raw_text = extract_text_from_pdf(file)
        text = clean_text(raw_text)
        chunks = simple_char_chunk(text)

        for i in tqdm(range(0, len(chunks), 50), desc=f"Indexing {file}"):
            batch = chunks[i:i+50]
            embeddings = embed_batch(batch)

            vectors = [{
                "id": str(uuid.uuid4()),
                "values": emb,
                "metadata": {"source": file.split('/')[-1], "text": chunk}
            } for emb, chunk in zip(embeddings, batch)]

            index.upsert(vectors)

    logger.info("Vector DB Build Complete ✔")

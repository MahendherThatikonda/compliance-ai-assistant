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

def retrieve(q):
    logger.info("Searching knowledge base...")
    res = index.query(vector=embed_query(q), top_k=TOP_K, include_metadata=True)
    return res.matches

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

PDF_FOLDER = os.getenv("PDF_FOLDER", "./PDFs/ALL_Foley_Files")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")

EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "1024"))
TOP_K = 5

#print(PDF_FOLDER)

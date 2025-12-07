import json
import chromadb
from chromadb.utils import embedding_functions

from ..utils_chroma.config_chroma import (
    VECTOR_DB_DIR, PROCESSED_DIR,
    OPENAI_API_KEY, EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME
)
from ..utils_chroma.logging_utils_chroma import get_logger
from .pdf_loader_chroma import list_pdfs, extract_text_from_pdf
from .text_splitter_chroma import clean_text, split_into_chunks

logger = get_logger(__name__)

def build_index():
    pdfs = list_pdfs()
    if not pdfs:
        logger.warning("No PDF files found — cannot build index.")
        return

    logger.info(f"Initialising Chroma at: {VECTOR_DB_DIR}")
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

    embedder = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL_NAME,
    )

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=embedder,
    )

    all_ids, all_docs, all_meta = [], [], []

    for pdf in pdfs:
        logger.info(f"Processing {pdf.name}")
        raw_text = extract_text_from_pdf(pdf)
        cleaned = clean_text(raw_text)
        chunks = split_into_chunks(cleaned)

        for i, chunk in enumerate(chunks):
            doc_id = f"{pdf.stem}_{i}"
            metadata = {"source": pdf.name, "chunk": i}

            all_ids.append(doc_id)
            all_docs.append(chunk)
            all_meta.append(metadata)

    logger.info(f"Adding {len(all_docs)} chunks to Chroma.")

    collection.add(
        ids=all_ids,
        documents=all_docs,
        metadatas=all_meta,
    )

    meta_path = PROCESSED_DIR / "metadata.json"
    meta_path.write_text(json.dumps(all_meta, indent=2), encoding="utf-8")

    logger.info(f"Index build complete. Metadata saved → {meta_path}")


if __name__ == "__main__":
    build_index()

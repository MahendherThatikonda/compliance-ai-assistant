# rag_chroma/ingestion_chroma/text_splitter_chroma.py

def clean_text(text: str) -> str:
    text = text.replace("\r", " ")
    text = text.replace("\n", " ")
    return " ".join(text.split())


def split_into_chunks(text: str, chunk_size=800, overlap=200):
    chunks = []
    start = 0
    length = len(text)

    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])

        if end == length:
            break

        start = end - overlap

    return chunks

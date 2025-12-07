def simple_char_chunk(text, max_chars=800, overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

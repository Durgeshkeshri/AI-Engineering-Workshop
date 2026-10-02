"""
chunker.py — Splits document text into overlapping character chunks.
"""

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50


def chunk_document(document: dict) -> list[dict]:
    """Splits a document dictionary into fixed-size overlapping text chunks."""
    text = document["text"]
    source = document["source"]
    chunks, start, index = [], 0, 0

    while start < len(text):
        chunk_text = text[start : start + CHUNK_SIZE].strip()
        if chunk_text:
            chunks.append({"source": source, "chunk_index": index, "text": chunk_text})
            index += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def chunk_all_documents(documents: list[dict]) -> list[dict]:
    """Chunks all documents and returns a flattened list of chunk dictionaries."""
    all_chunks = []
    for doc in documents:
        doc_chunks = chunk_document(doc)
        all_chunks.extend(doc_chunks)
        print(f"  ✂  {doc['source']} → {len(doc_chunks)} chunks")

    print(f"\n  Total chunks: {len(all_chunks)}")
    return all_chunks

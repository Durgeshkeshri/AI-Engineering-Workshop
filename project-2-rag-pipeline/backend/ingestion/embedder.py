"""
embedder.py — Generates Gemini dense vector embeddings for document chunks and user queries.
"""

from google import genai
from config import settings

client = genai.Client(api_key=settings.gemini_api_key)


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Generates RETRIEVAL_DOCUMENT embeddings for a list of chunk dicts."""
    print(f"\n🔢 Embedding {len(chunks)} chunks …")
    for i, chunk in enumerate(chunks):
        result = client.models.embed_content(
            model=settings.gemini_embedding_model,
            contents=chunk["text"],
            config={"task_type": "RETRIEVAL_DOCUMENT"},
        )
        chunk["embedding"] = result.embeddings[0].values
        if (i + 1) % 10 == 0 or (i + 1) == len(chunks):
            print(f"  … {i + 1}/{len(chunks)} embedded")

    return chunks


def embed_query(question: str) -> list[float]:
    """Generates RETRIEVAL_QUERY vector embedding for a user question."""
    result = client.models.embed_content(
        model=settings.gemini_embedding_model,
        contents=question,
        config={"task_type": "RETRIEVAL_QUERY"},
    )
    return result.embeddings[0].values

"""
vector_store.py — Persistent ChromaDB collection wrapper for vector search.
"""

import chromadb
from config import settings


def _get_collection() -> chromadb.Collection:
    """Returns or initializes the local persistent ChromaDB collection."""
    chroma_client = chromadb.PersistentClient(path=str(settings.chroma_db_dir))
    return chroma_client.get_or_create_collection(
        name=settings.chroma_collection,
        metadata={"hnsw:space": "cosine"},
    )


def store_chunks(chunks: list[dict]) -> int:
    """Upserts embedded document chunks into ChromaDB and returns total collection count."""
    collection = _get_collection()
    collection.upsert(
        ids=[f"{c['source']}__chunk_{c['chunk_index']}" for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} for c in chunks],
    )
    return collection.count()


def query_collection(query_embedding: list[float], top_k: int) -> dict:
    """Performs cosine similarity search against ChromaDB."""
    return _get_collection().query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )


def collection_count() -> int:
    """Returns total stored chunk count in ChromaDB."""
    return _get_collection().count()


def get_stored_sources() -> dict:
    """Returns {filename: chunk_count} mapping for active documents in ChromaDB."""
    data = _get_collection().get(include=["metadatas"])
    doc_counts = {}
    if data and data.get("metadatas"):
        for meta in data["metadatas"]:
            src = meta.get("source", "Unknown Document")
            doc_counts[src] = doc_counts.get(src, 0) + 1

    return doc_counts

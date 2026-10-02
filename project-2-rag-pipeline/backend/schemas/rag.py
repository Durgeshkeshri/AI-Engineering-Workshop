"""
rag.py — Pydantic request and response models for RAG pipeline.
"""

from pydantic import BaseModel


# ── Ingest ────────────────────────────────────────────────────────────────────

class IngestResponse(BaseModel):
    message: str
    documents_ingested: int
    chunks_stored: int


# ── Sources ───────────────────────────────────────────────────────────────────

class SourceDocInfo(BaseModel):
    filename: str
    chunk_count: int


class SourcesResponse(BaseModel):
    documents: list[SourceDocInfo]
    total_chunks: int


# ── Query ─────────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str
    top_k: int | None = None


class SourceChunk(BaseModel):
    source: str       # original filename
    chunk_index: int  # position inside the document
    score: float      # similarity distance (lower = more similar in ChromaDB)
    text: str         # the actual chunk text


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    declined: bool = False   # True when no relevant context was found

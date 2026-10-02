"""
sources.py — GET /sources

Returns active source document metadata and chunk count.
"""

from fastapi import APIRouter

from retrieval.vector_store import get_stored_sources, collection_count
from schemas.rag import SourcesResponse, SourceDocInfo

router = APIRouter()


@router.get("/sources", response_model=SourcesResponse)
async def list_sources():
    doc_counts = get_stored_sources()
    documents = [
        SourceDocInfo(filename=fname, chunk_count=count)
        for fname, count in doc_counts.items()
    ]
    return SourcesResponse(
        documents=documents,
        total_chunks=collection_count()
    )

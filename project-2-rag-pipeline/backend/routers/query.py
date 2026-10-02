"""
query.py — POST /query

Handles a user question end-to-end:
  Question → embed query → retrieve top-k chunks → generate grounded answer
"""

from fastapi import APIRouter, HTTPException

from retrieval.retriever import retrieve, generate_answer
from retrieval.vector_store import collection_count
from schemas.rag import QueryRequest, QueryResponse, SourceChunk

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query(body: QueryRequest):
    """
    Retrieve relevant document chunks and generate a grounded answer.

    Steps:
      1. Embed the question  (embedder.embed_query)
      2. Retrieve top-k similar chunks  (retriever.retrieve)
      3. Generate the reply; the model classifies small talk / policy / out-of-scope
      4. Return the reply, with source citations only when policy chunks were used
    """
    if collection_count() == 0:
        raise HTTPException(
            status_code=400,
            detail="Vector store is empty. Please call POST /ingest first.",
        )

    try:
        # Retrieve
        chunks = retrieve(body.question, top_k=body.top_k)

        # Generate
        answer, declined, used_chunks = generate_answer(body.question, chunks)

        # Format source citations
        sources = [
            SourceChunk(
                source=c["source"],
                chunk_index=c["chunk_index"],
                score=round(c["score"], 4),
                text=c["text"],
            )
            for c in used_chunks
        ]

        return QueryResponse(answer=answer, sources=sources, declined=declined)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

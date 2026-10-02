"""
ingest.py — POST /ingest

Triggers the full ingestion pipeline:
  PDF files → LLM extraction → chunking → embedding → ChromaDB storage

This endpoint is designed to be called once (or whenever source docs change).
It is idempotent because ChromaDB uses upsert — running it again will simply
overwrite the existing embeddings for the same chunk IDs.
"""

from fastapi import APIRouter, HTTPException

from ingestion.loader import load_all_pdfs
from ingestion.chunker import chunk_all_documents
from ingestion.embedder import embed_chunks
from retrieval.vector_store import store_chunks
from schemas.rag import IngestResponse

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
async def ingest():
    """
    Run the full ingestion pipeline on all PDFs in source_docs_dir.

    Steps:
      1. Load & LLM-parse every PDF  (loader.py)
      2. Split into overlapping text chunks  (chunker.py)
      3. Embed each chunk via Gemini  (embedder.py)
      4. Upsert into ChromaDB  (vector_store.py)
    """
    try:
        # Phase 1 — Load
        documents = load_all_pdfs()

        # Phase 2 — Chunk
        print("\n✂  Chunking documents …")
        chunks = chunk_all_documents(documents)

        # Phase 3 — Embed
        chunks_with_embeddings = embed_chunks(chunks)

        # Phase 4 — Store
        print("\n💾 Storing in ChromaDB …")
        total_stored = store_chunks(chunks_with_embeddings)
        print(f"  ✓ ChromaDB now contains {total_stored} chunks total.")

        return IngestResponse(
            message="Ingestion complete.",
            documents_ingested=len(documents),
            chunks_stored=len(chunks),
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

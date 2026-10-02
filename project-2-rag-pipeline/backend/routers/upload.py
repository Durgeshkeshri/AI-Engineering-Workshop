"""
upload.py — POST /upload

Upload a PDF document, save it locally to backend/data/source-docs,
and automatically re-ingest all documents into ChromaDB.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException

from config import settings
from ingestion.loader import load_all_pdfs
from ingestion.chunker import chunk_all_documents
from ingestion.embedder import embed_chunks
from retrieval.vector_store import store_chunks

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF policy document, save it to source_docs_dir,
    and automatically trigger complete RAG re-ingestion.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF documents (.pdf) are supported.",
        )

    try:
        # 1. Ensure source_docs_dir exists
        settings.source_docs_dir.mkdir(parents=True, exist_ok=True)

        # 2. Save file locally
        target_path = settings.source_docs_dir / file.filename
        content = await file.read()
        with open(target_path, "wb") as f:
            f.write(content)

        print(f"📥 Saved uploaded PDF to: {target_path}")

        # 3. Trigger automatic re-ingestion
        print("\n🚀 Running automatic re-ingestion after file upload...")
        documents = load_all_pdfs()
        chunks = chunk_all_documents(documents)
        chunks_with_embeddings = embed_chunks(chunks)
        total_stored = store_chunks(chunks_with_embeddings)

        print(f"✓ Upload & Ingestion complete. ChromaDB contains {total_stored} chunks.")

        return {
            "message": f"Successfully uploaded and ingested {file.filename}.",
            "filename": file.filename,
            "documents_total": len(documents),
            "chunks_stored": total_stored,
        }

    except Exception as e:
        print(f"❌ Upload/Ingestion failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload & Ingestion failed: {e}",
        )

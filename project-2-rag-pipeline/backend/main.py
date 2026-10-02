import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import ingest, query, sources, upload
from retrieval.vector_store import collection_count, store_chunks
from ingestion.loader import load_all_pdfs
from ingestion.chunker import chunk_all_documents
from ingestion.embedder import embed_chunks

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Automatic startup document ingestion if ChromaDB is empty."""
    logger.info("Initializing RAG vector database...")
    try:
        count = collection_count()
        if count == 0:
            logger.info("⚡ Vector database is empty. Running automatic startup ingestion on source PDFs...")
            docs = load_all_pdfs()
            chunks = chunk_all_documents(docs)
            chunks_with_emb = embed_chunks(chunks)
            stored = store_chunks(chunks_with_emb)
            logger.info(f"✓ Startup ingestion complete! ChromaDB now contains {stored} chunks.")
        else:
            logger.info(f"✓ Vector database already populated ({count} chunks). Ready!")
    except Exception as e:
        logger.error(f"⚠ Startup document ingestion error: {e}")
    yield


app = FastAPI(
    title="Bharati Vidyapeeth RAG Pipeline",
    description="Retrieval-Augmented Generation over Bharati Vidyapeeth policy documents.",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(sources.router)
app.include_router(upload.router)


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "project": "RAG Pipeline — Bharati Vidyapeeth",
        "chunk_count": collection_count(),
    }


# Serve frontend UI at http://localhost:8001
frontend_dir = Path(__file__).parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


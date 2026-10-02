# Project 2 — Production RAG Pipeline (Bharati Vidyapeeth Policy Assistant)

A full-stack, enterprise-grade Retrieval-Augmented Generation (RAG) system built over real institutional policy documents of Bharati Vidyapeeth.

---

## 🌟 Overview & Key Architecture

```
[ PDF Documents ] ──► [ Gemini File API / Parser ] ──► [ Text Chunker ]
                                                              │
                                                              ▼
[ Grounded Answer ] ◄── [ Gemini 2.5 Flash ] ◄── [ ChromaDB Vector Store ] ◄── [ Gemini Embeddings ]
```

### Key Highlights

- **LLM-Powered PDF Ingestion**: Uses Gemini API to extract clean, structured text directly from complex multipage PDFs.
- **Overlapping Window Chunking**: Splits extracted document text into ~1500 character chunks with 200 character overlaps, retaining headers and metadata context.
- **Asymmetric Vector Embeddings**: Uses `text-embedding-004` with explicit Gemini task types:
  - `RETRIEVAL_DOCUMENT` during ingestion
  - `RETRIEVAL_QUERY` during user search
- **Vector DB Storage**: Persistent ChromaDB instance storing cosine distance vector embeddings and metadata.
- **Strict Grounding & Anti-Hallucination**: Employs similarity threshold filtering (`<= 0.5`) + XML-structured prompts (`<context>`, `<chunk>`, `<question>`). If no relevant source context is found, the assistant declines politely instead of guessing.
- **Prompt Externalization**: System instructions and PDF extraction prompts are maintained in separate prompt text files (`backend/prompts/`).

---

## 📁 Directory Structure

```
project-2-rag-pipeline/
├── backend/
│   ├── config/
│   │   └── settings.py        # Configuration & Environment loading (find_dotenv)
│   ├── main.py                # FastAPI app entrypoint with CORS & Static files
│   ├── data/
│   │   ├── source-docs/       # PDF document storage
│   │   └── chroma_db/         # Persisted ChromaDB vector database
│   ├── prompts/
│   │   ├── system_prompt.txt     # Grounded system prompt instruction
│   │   └── extraction_prompt.txt # LLM PDF text extraction prompt
│   ├── ingestion/
│   │   ├── loader.py          # PDF extraction via Gemini File API
│   │   ├── chunker.py         # Overlapping text chunker
│   │   └── embedder.py        # Gemini vector embedding generator
│   ├── retrieval/
│   │   ├── vector_store.py    # ChromaDB collection wrapper
│   │   └── retriever.py       # Similarity search & grounded answer generation
│   ├── routers/
│   │   ├── ingest.py          # POST /ingest endpoint
│   │   ├── query.py           # POST /query endpoint
│   │   ├── sources.py         # GET /api/sources endpoint
│   │   └── upload.py          # POST /api/upload endpoint
│   └── schemas/
│       └── rag.py             # Pydantic models for API request/response
├── frontend/
│   ├── index.html             # Web UI structure
│   ├── style.css              # Dark mode glassmorphism styling
│   └── app.js                 # Dynamic UI logic & backend integration
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.10+
- Valid `GEMINI_API_KEY` set in workspace root `.env` file

---

### Step 1: Start the Server

####  macOS / 🐧 Linux
```bash
cd project-2-rag-pipeline/backend

# Using virtualenv python directly (no activation needed)
PYTHONPATH=. ../../venv/bin/uvicorn main:app --reload --port 8001

# OR: Activate first, then run
source ../../venv/bin/activate
uvicorn main:app --reload --port 8001
```

#### 🪟 Windows (Command Prompt / CMD)
```cmd
cd project-2-rag-pipeline\backend
..\..\venv\Scripts\activate.bat
set PYTHONPATH=.
uvicorn main:app --reload --port 8001
```

---

### Step 2: Open the Web Application

Navigate to **`http://localhost:8001`** in your browser.

> The FastAPI server automatically hosts both the backend REST API and the frontend UI.

---

## ⚡ API Endpoints

### 1. Ingest Documents (`POST /ingest`)

Triggers full PDF extraction, chunking, embedding, and storage in ChromaDB:

```bash
curl -X POST http://localhost:8001/ingest
```

**Response:**

```json
{
  "message": "Ingestion complete.",
  "documents_ingested": 4,
  "chunks_stored": 28
}
```

---

### 2. Query RAG System (`POST /query`)

Ask questions based on the ingested policy documents:

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the minimum attendance required for examinations?"}'
```

**Response:**

```json
{
  "answer": "As per Examination_Rules.pdf [Chunk 1], students must maintain a minimum of 75% attendance in each subject to be eligible for end-semester examinations.",
  "declined": false,
  "sources": [
    {
      "source": "Examination_Rules.pdf",
      "chunk_index": 0,
      "score": 0.24,
      "text": "..."
    }
  ]
}
```

---

## 🛠 Features & Verification

- **Real Document Processing**: Ingests actual college PDFs located in `backend/data/source-docs/`.
- **Source Citation**: Every response highlights exact source PDF names, chunk indices, and cosine similarity match scores.
- **Anti-Hallucination Safe Mode**: Try asking *"What is the recipe for chocolate cake?"* — the model will respond stating that the provided documents do not contain information to answer the question.

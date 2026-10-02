# Project 2 — Production RAG Pipeline (Bharati Vidyapeeth Policy Assistant)

A full-stack, enterprise-grade Retrieval-Augmented Generation (RAG) system built over real institutional policy documents of Bharati Vidyapeeth.

---

## 🌟 Overview & Key Architecture

```
[ PDF Documents ] ──► [ Gemini File API / Parser ] ──► [ Text Chunker ]
                                                              │
                                                              ▼
[ Grounded Answer ] ◄── [ Gemini ] ◄── [ ChromaDB Vector Store ] ◄── [ Gemini Embeddings ]
```

### Key Highlights

- **LLM-Powered PDF Ingestion**: Uses Gemini API to extract clean, structured text directly from complex multipage PDFs.
- **Overlapping Window Chunking**: Splits extracted document text into fixed-size chunks of 400 characters with a 50 character overlap (`ingestion/chunker.py`). Chunks are cut by character count, so a sentence can be split across two chunks.
- **Asymmetric Vector Embeddings**: Uses the embedding model set in `GEMINI_EMBEDDING_MODEL` with explicit Gemini task types:
  - `RETRIEVAL_DOCUMENT` during ingestion
  - `RETRIEVAL_QUERY` during user search
- **Vector DB Storage**: Persistent ChromaDB instance storing cosine distance vector embeddings and metadata.
- **Strict Grounding & Anti-Hallucination**: Chunks are filtered by a distance threshold (`relevance_threshold`, default `0.5`, lower = more similar) and passed to the model in XML tags (`<context>`, `<chunk>`, `<question>`). The prompt tells the model to state only facts found in the context and never to infer.
- **Conversational Persona with Structured Output**: The assistant (Aria) can handle small talk as well as policy questions. Each reply comes back as JSON (`reasoning`, `intent`, `answer`) enforced by a Pydantic schema. The `intent` is one of `small_talk`, `policy_question`, `partial_answer` or `out_of_scope`, and the backend uses it to decide whether to return sources and whether to mark the reply as declined.
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
│   │   ├── sources.py         # GET /sources endpoint
│   │   └── upload.py          # POST /upload endpoint
│   └── schemas/
│       └── rag.py             # Pydantic models for API request/response
├── frontend/
│   ├── index.html             # Web UI structure
│   ├── style.css              # Light, neutral styling
│   └── app.js                 # Dynamic UI logic & backend integration
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.10+
- A workspace root `.env` file with:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=<gemini model name>
GEMINI_EMBEDDING_MODEL=<gemini embedding model name>
```

Optional settings (defaults in `backend/config/settings.py`): `TOP_K` (default 3) and `RELEVANCE_THRESHOLD` (default 0.5).

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
>
> The vector index (`backend/data/chroma_db/`) is not stored in git. On first start the server finds it empty and builds it from the PDFs in `backend/data/source-docs/` automatically. This takes a while, because every PDF and chunk is sent to Gemini. You can also rebuild it any time with `POST /ingest` or the **Rebuild index** button in the UI.

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
  "documents_ingested": 5,
  "chunks_stored": 26
}
```

---

### 2. Query RAG System (`POST /query`)

Ask questions based on the ingested policy documents:

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the minimum attendance required for examinations?", "top_k": 3}'
```

`top_k` is optional (it falls back to the server default) and is controlled by the **Passages retrieved** slider in the UI.

**Response:**

```json
{
  "answer": "According to Examination_Policy.pdf, a minimum of **75% attendance** in a course is required to sit its semester examination...",
  "declined": false,
  "sources": [
    {
      "source": "Examination_Policy.pdf",
      "chunk_index": 0,
      "score": 0.24,
      "text": "..."
    }
  ]
}
```

`score` is a cosine distance (lower = more similar). The values shown are illustrative.

**How the response fields behave**

| Message type | `declined` | `sources` |
|---|---|---|
| Small talk ("Hello") | `false` | empty |
| Fully answered policy question | `false` | the chunks used |
| Partly answered ("exact deadline", when the documents only give the month) | `false` | the chunks used |
| Out of scope (not in the documents) | `true` | empty |

---

### 3. Other endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/sources` | Lists indexed documents and their chunk counts. |
| `POST` | `/upload` | Uploads a PDF, saves it to `backend/data/source-docs/`, and re-indexes everything. |
| `GET` | `/api/health` | Health check, including the number of indexed chunks. |

---

## 🛠 Features & Verification

- **Real Document Processing**: Ingests actual college PDFs located in `backend/data/source-docs/`.
- **Source Citation**: Every response highlights exact source PDF names, chunk indices, and cosine similarity match scores.
- **Anti-Hallucination Safe Mode**: Try asking *"What is the recipe for chocolate cake?"* — the assistant will say it doesn't have that information in the college documents and will not show any sources.
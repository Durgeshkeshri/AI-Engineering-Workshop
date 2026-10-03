# AI Engineering Workshop — Gemini API & RAG Pipelines

**Bharati Vidyapeeth**

A comprehensive, hands-on workshop repository covering LLM fundamentals, prompt engineering, structured outputs, multimodal inputs, token usage, guardrails, context caching, tool calling, multi-turn AI agents, and production RAG pipelines using Google's **Gemini AI API** (`google-genai` SDK).

---

## 🔑 How to Get Your Gemini API Key

1. Go to **Google AI Studio**: [https://aistudio.google.com/](https://aistudio.google.com/)
2. Sign in with your Google Account.
3. Click on **"Get API key"** in the top navigation bar.
4. Click **"Create API key"** (select an existing Google Cloud project or create a new one).
5. Copy your API Key string (starts with `AIzaSy...`). You will place this inside your `.env` file.

---

## 🚀 Environment Setup

### 1. Prerequisites
- **Python 3.10+** (Verify with `python3 --version` or `python --version`)
- **Git** installed

---

### 2. Create and Activate Virtual Environment (`venv`)

#### 🍏 macOS / 🐧 Linux
```bash
# 1. Navigate to the repository root directory
cd Workshop

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate
```

#### 🪟 Windows (Command Prompt / CMD)
```cmd
:: 1. Navigate to the repository root directory
cd Workshop

:: 2. Create virtual environment
python -m venv venv

:: 3. Activate virtual environment
venv\Scripts\activate
```

---

### 3. Install Dependencies

Once your virtual environment is active (you will see `(venv)` at the start of your terminal prompt), run:

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables (`.env`)

Create a `.env` file in the repository root directory (`Workshop/.env`):

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-3.8-flash
EMBEDDING_MODEL=text-embedding-004
```

> ⚠️ **Note**: Replace `your_actual_api_key_here` with your real Google AI Studio key. Never commit your `.env` file to Git!

---

## 📚 Workshop Modules & Projects Overview

| Directory | Topic | Description |
| :--- | :--- | :--- |
| [`01-prompt-engineering`](./01-prompt-engineering) | **Prompt Engineering** | Zero-shot, Few-shot, Chain of Thought, and XML structuring. |
| [`02-llm-request-response`](./02-llm-request-response) | **LLM Request & Response** | Inspecting Gemini SDK request payloads and candidate responses. |
| [`03-sampling-top-p-top-k`](./03-sampling-top-p-top-k) | **Sampling Parameters** | Temperature, `top_p`, and `top_k` sampling effects on response creativity. |
| [`04-structured-output-pydantic`](./04-structured-output-pydantic) | **Structured Outputs** | Enforcing strict typed JSON output schemas using Pydantic. |
| [`05-multimodal-input`](./05-multimodal-input) | **Multimodal Input** | Image and audio file processing alongside text prompts. |
| [`06-token-usage`](./06-token-usage) | **Token Usage Tracking** | Inspecting prompt and candidate token metrics across modalities. |
| [`07-token-limit`](./07-token-limit) | **Token Limits** | Controlling `max_output_tokens` and handling truncation finish reasons. |
| [`08-prompt-guardrails`](./08-prompt-guardrails) | **Guardrails & Safety** | Persona boundaries, system scope enforcement, and harm category filters. |
| [`09-caching`](./09-caching) | **Context Caching** | Server-side document caching (`client.caches`) for latency & cost reduction. |
| [`10-tool-calling`](./10-tool-calling) | **Tool Calling (Function Calling)** | Schema declaration (`types.Tool`), manual execution dispatch, and response synthesis. |
| [`project-1-chatbot-agent`](./project-1-chatbot-agent) | **Project 1 — ChatBot Agent** | Multi-turn agent with custom tools (FAQ search, calculator, IST datetime) and web search grounding. |
| [`project-2-rag-pipeline`](./project-2-rag-pipeline) | **Project 2 — RAG Pipeline** | Semantic document parsing, chunking, ChromaDB vector retrieval, grounded generation, and Vanilla JS UI. |

---

## 💻 How to Run

Make sure your `venv` is active (`source venv/bin/activate` or `venv\Scripts\activate`) before running any script.

### Running Hands-on Modules (01 - 10)

Run scripts directly from the **repository root**:

```bash
# Module 01 — Prompt Engineering
python 01-prompt-engineering/main.py

# Module 04 — Structured Output
python 04-structured-output-pydantic/main.py

# Module 09 — Context Caching
python 09-caching/create_cache.py
python 09-caching/query_cache.py

# Module 10 — Tool Calling Console Demo
python 10-tool-calling/main.py
```

---

### Running Project 1 — ChatBot Agent

#### Option A: Terminal Console Mode
```bash
python project-1-chatbot-agent/main.py
```

#### Option B: Web Backend & Frontend (FastAPI)
```bash
# Start FastAPI web server on port 8000
cd project-1-chatbot-agent/backend && uvicorn main:app --reload --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your web browser.

---

### Running Project 2 — RAG Pipeline

#### Start RAG FastAPI Web Backend & Frontend UI
```bash
# Start RAG pipeline server on port 8001
cd project-2-rag-pipeline/backend && uvicorn main:app --reload --port 8001
```
Open **[http://localhost:8001](http://localhost:8001)** in your web browser.

- **POST `/ingest`**: Triggers batch document loading, chunking, embedding, and vector storage.
- **POST `/query`**: Runs semantic similarity search against ChromaDB and generates grounded answers with citations.

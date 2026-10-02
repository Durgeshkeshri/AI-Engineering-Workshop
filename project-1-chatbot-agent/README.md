# Project 1 — ChatBot Agent (Bharati Vidyapeeth AI Assistant)

A multi-turn conversational AI chatbot built with **Google Gemini API**, implementing a full **Plan → Act → Observe** agent loop with native tool calling capabilities — now featuring a **FastAPI web backend + rich browser UI** and real-time **Google Web Search** grounding.

---

## 🌟 Overview & Key Concepts

```
[ Browser UI ] ──► [ FastAPI /chat ] ──► [ Gemini API ] ──► Tool needed?
                                               │                    │
                              ┌────────────────┤ Yes                │ No
                              │                ▼                    ▼
                              │   [ Dispatch local tool ]    [ Final Answer ]
                              │           │                        │
                              └───────────┴────── ► [ Feed result → Gemini ]
```

### Key Concepts Covered

- **System Prompting** — Persona definition, constraints, and scope boundaries.
- **Multi-Turn Memory** — Session-based conversation history (`role: user / model`).
- **Function Calling & Tool Declarations** — `FunctionDeclaration` schemas for local Python tools.
- **Native Google Search Grounding** — `types.Tool(google_search=types.GoogleSearch())` enables real-time web results without any extra API key.
- **Agent Loop (Plan → Act → Observe)** — Detects tool calls, executes them locally, feeds results back to Gemini.
- **FastAPI Web Server** — REST API with session management; serves the SPA frontend.

---

## 📁 Directory Structure

```
project-1-chatbot-agent/
├── backend/
│   ├── main.py          # FastAPI application entrypoint (CORS, router inclusion, SPA serving)
│   ├── routes/
│   │   └── chat.py      # Chat & health API routes (POST /chat, GET /health)
│   ├── memory.py        # In-memory session store (get_history)
│   ├── model/
│   │   └── model.py     # Pydantic request & response data models (ChatRequest, ChatResponse)
│   ├── config/
│   │   └── settings.py  # Environment settings loader (GEMINI_API_KEY, GEMINI_MODEL)
│   ├── tools/
│   │   └── tools.py     # Consolidated local tool functions, Gemini schemas, and TOOL_REGISTRY
│   ├── utils/
│   │   └── helpers.py   # Helper utilities (dispatch_tool_call, extract_citations)
│   ├── agent/
│   │   └── agent_loop.py# Plan → Act → Observe loop + google_search grounding
│   ├── prompts/
│   │   └── system_prompt.txt# Bharati Vidyapeeth assistant persona, scope rules, tool guidance
│   └── data/
│       └── faq.json     # Bharati Vidyapeeth policy & department FAQ database
└── frontend/
    ├── index.html       # SPA chat interface
    ├── style.css        # Light, neutral stylesheet
    └── app.js           # Chat logic, markdown rendering, tool badges
```

---

## 🚀 How to Run (Cross-Platform)

### Step 0: Prerequisites

Make sure your `.env` file exists in the workspace root (`../../`) with:

```
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

---

### Step 1: Start the FastAPI Backend

#### macOS / 🐧 Linux

```bash
cd project-1-chatbot-agent/backend

# Using virtualenv python directly (no activation needed)
PYTHONPATH=. ../../venv/bin/uvicorn main:app --reload --port 8000

# OR: Activate first, then run
source ../../venv/bin/activate
uvicorn main:app --reload --port 8000
```

#### 🪟 Windows (Command Prompt / CMD)

```cmd
cd project-1-chatbot-agent\backend
..\..\venv\Scripts\activate.bat
set PYTHONPATH=.
uvicorn main:app --reload --port 8000
```

---

### Step 2: Open the Browser UI

Once the server is running, open your browser and navigate to:

```
http://localhost:8000
```

The FastAPI server automatically serves the frontend — no separate web server needed.

---

## 🛠 API Endpoints

| Method     | Endpoint                       | Description                                                                                   |
| ---------- | ------------------------------ | --------------------------------------------------------------------------------------------- |
| `POST`   | `/chat`                      | Send a message. Body:`{"message": "...", "session_id": "..."}`. Returns reply + tools_used. |
| `GET`    | `/health`                    | Health check. Returns`{"status": "ok"}`.                                                    |
| `GET`    | `/`                          | Serves the browser UI.                                                                        |

---

## 🔧 Available Tools

| Tool                     | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `get_current_datetime` | Returns current date & time in IST                            |
| `calculate`            | Evaluates arithmetic expressions (parsed safely, no `eval`)   |
| `search_faq`           | Searches the Bharati Vidyapeeth FAQ knowledge base            |
| `google_search`        | Native Gemini Google Search grounding (real-time web results) |

---

## 📝 Notes

- **Session management** is in-memory and resets on server restart.
- **Grounding:** College-specific facts must come from `search_faq` or web search, not from the model's memory. The prompt (`backend/prompts/system_prompt.txt`) tells the model to say where facts came from, not to infer, and to point users to the administration when sources don't answer.
- **`calculate`** parses the expression with Python's `ast` module and allows only numbers and `+ - * / // % **`, so model-generated text is never run as code.
- **`search_faq`** is a simple keyword match that returns the first FAQ entry sharing a word with the query. It is fine for a small demo FAQ but can match unrelated entries on common words.
- **New chat:** The **New chat** button asks for confirmation (the old conversation is lost), clears the screen, and drops the session ID, so the next message starts a fresh session. The previous session's history stays in server memory until the server restarts.
- The **Google Search** grounding uses Gemini's built-in capability — no Search API key required.

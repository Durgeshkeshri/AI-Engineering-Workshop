# 09 — Context Caching

## Goal
Learn how to use **context caching** to upload a large document to the Gemini server **once**, and query it **multiple times** with different questions — without re-sending the document on every request. This reduces token cost and latency.

## Concepts Covered
- `client.caches.create()` — uploads content to the Gemini server with a TTL
- `client.caches.list()` — lists all active server caches
- `cached_content` in `GenerateContentConfig` — attaches a cache to a generate request
- `ttl` — how long the cache lives on the server before expiring
- `usage_metadata.cached_content_token_count` — tokens served from cache (billed at a discounted rate)

## Prerequisite
`08-prompt-guardrails`

## Files

| File | Purpose |
|------|---------|
| `create_cache.py` | Uploads `source-docs/knowledge_base.txt` to the Gemini server and creates a cache |
| `query_cache.py` | Finds the active cache and sends a query against it |

## How to Run

> Run from the **repo root** (`Workshop/` folder).

### Step 1 — Create the cache (run once)

**Mac / Linux**
```bash
source venv/bin/activate
python3 09-caching/create_cache.py
```

**Windows**
```cmd
venv\Scripts\activate
python 09-caching/create_cache.py
```

Expected output:
```
Cache Name   : cachedContents/xxxx
Cached Tokens: 4788
Expires at   : 2026-09-30 17:10:22
```

---

### Step 2 — Query the cache (run as many times as you like)

```bash
python3 09-caching/query_cache.py
```

Expected output:
```
Cache Name : cachedContents/xxxx
Expires at : 2026-09-30 17:10:22

--- RESPONSE ---
Context Caching is a feature that allows developers to store a large,
repeated portion of input context on the server side...

Cached tokens : 4788   ← document served from cache, not re-sent
Output tokens : 81     ← only your question + answer are new tokens
```

> **The `prompt` in `query_cache.py` can be any question about the document** — the cached 4788 tokens are always reused regardless of what you ask.

---

## How It Works

```
create_cache.py         Gemini Server
      │                         │
      │── caches.create() ─────►│  Stores document (4788 tokens) for 10 mins
      │◄── cache.name ──────────│
      │
      ▼
query_cache.py
      │
      │── caches.list() ───────►│  Finds active cache by display_name
      │── generate_content() ──►│  Sends only your question (~5 tokens)
      │                         │  Server reads document from cache
      │◄── response ────────────│
```

## Challenge

Change `ttl="600s"` to `ttl="30s"` in `create_cache.py`, run it, wait 35 seconds, then run `query_cache.py` — observe what happens when the cache expires!

# 06 — Token Usage

## Goal
Understand how different input modalities (text, image, audio) consume different amounts of tokens, and how to read the full token breakdown from `usage_metadata`.

## Concepts Covered
- `usage_metadata` on the response — `prompt_token_count`, `candidates_token_count`, `thoughts_token_count`, `total_token_count`
- `prompt_tokens_details` — per-modality breakdown (TEXT / IMAGE / AUDIO)
- `cached_content_token_count` — tokens served from context cache (cheaper)
- How thinking/reasoning tokens contribute to total cost

## Prerequisite
`05-multimodal-input`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 06-token-usage/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 06-token-usage/main.py
```

## What to Observe
- **Text only:** only `Input (TEXT)` is shown — cheapest call
- **Image + Text:** `Input (IMAGE)` adds ~1 100 tokens for a small JPEG — images are expensive
- **Audio + Text:** `Input (AUDIO)` adds ~15 000 tokens for a few minutes of audio — very token-heavy
- **Thoughts:** Gemini 3.8 Flash uses internal reasoning tokens (`thoughts_token_count`) not visible in the response text but counted toward total cost
- **Cached:** The audio call may show `Cached Input` tokens — these are billed at a reduced rate

## Challenge
1. Swap the image for a larger photo — how does `Input (IMAGE)` token count change?
2. Trim the audio to 30 seconds and re-run — how much cheaper is the audio call?
3. Add a fourth call that sends both image and audio together. What does the token breakdown look like?

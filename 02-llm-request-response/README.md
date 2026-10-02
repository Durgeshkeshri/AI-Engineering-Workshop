# 02 — LLM Request/Response

## Goal
Understand the anatomy of an API call — what you send in a request and what comes back in the response object beyond just the text.

## Concepts Covered
- Request structure: `model`, `contents`
- Response object: `text`, `candidates`, `finish_reason`
- Token usage: `prompt_token_count`, `candidates_token_count`, `total_token_count`

## Prerequisite
`01-prompt-engineering`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 02-llm-request-response/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 02-llm-request-response/main.py
```

## What to Observe
- The response is more than just text — it carries metadata about *why* the model stopped and *how many tokens* were consumed.
- `finish_reason: STOP` means the model finished naturally. Other values like `MAX_TOKENS` mean it was cut off.
- Prompt tokens + output tokens = total tokens. This is what API pricing is based on.

## Challenge
1. Change the prompt to ask for a 10-sentence answer. Re-run and compare `output tokens` — does a longer answer cost more?
2. Change the prompt to something very short like `"Hi"`. What is the minimum token cost?
3. Look at `finish_reason` — change `contents` to a very long prompt that forces the model to hit a token limit and see the value change.

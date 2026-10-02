# 07 — Token Limit

## Goal
Understand how to configure output token limits (`max_output_tokens`) and inspect `finish_reason` to detect when a model's response is completed naturally (`STOP`) versus cut off early (`MAX_TOKENS`).

## Concepts Covered
- `max_output_tokens` in `GenerateContentConfig` — caps maximum tokens the model can generate
- `finish_reason` — indicates why generation ended (`STOP` vs `MAX_TOKENS`)
- Token usage metadata (`prompt_token_count`, `thoughts_token_count`, `candidates_token_count`, `total_token_count`)

## Prerequisite
`06-token-usage`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 07-token-limit/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 07-token-limit/main.py
```

## What to Observe

- **Response Truncation:** When `max_output_tokens=200`, the response may be cut off mid-sentence.
- **`finish_reason`:** 
  - `MAX_TOKENS`: Generation stopped because it hit the `max_output_tokens` limit.
  - `STOP`: Generation completed naturally before reaching the token cap.
- **Token Breakdown:** Inspect `prompt_token_count`, `thoughts_token_count`, and `candidates_token_count` printed in the output.

## Challenge

1. **Test Lower Cap:** Change `max_output_tokens` on line 15 of `main.py` to `30`. Re-run `main.py` and observe the truncated text and `finish_reason`.
2. **Test Higher Cap:** Increase `max_output_tokens` to `1000`. Observe how the response finishes naturally and `finish_reason` changes to `STOP`.

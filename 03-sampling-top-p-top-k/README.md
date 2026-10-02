# 03 — Sampling: Temperature, Top-p, Top-k

## Goal
Understand how `temperature`, `top_p`, and `top_k` control how random or deterministic the model's output is.

## Concepts & Parameter Ranges
- **Temperature** (Min: `0.0`, Max: `2.0`) — scales the probability distribution over tokens.
  - `0.0` (Min): Deterministic — always picks the single most probable token (greedy decoding).
  - `2.0` (Max): Highly creative/random — flattens probability distribution for diverse outputs.
- **Top-p / Nucleus Sampling** (Min: `0.0`, Max: `1.0`) — restricts token selection to the smallest set whose cumulative probability ≥ `p`.
  - `0.0` (Min): Restricts candidate pool to only the top token.
  - `1.0` (Max): Considers all candidate tokens up to 100% cumulative probability mass.
- **Top-k** (Min: `1`, Max: `40`) — restricts candidate token selection to the top `k` most probable tokens.
  - `1` (Min): Selects only from the top 1 token.
  - `40` (Max): Selects from the top 40 candidate tokens.

## Prerequisite
`02-llm-request-response`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 03-sampling-top-p-top-k/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 03-sampling-top-p-top-k/main.py
```

## What to Observe
Change `TEMPERATURE` and re-run multiple times:
- `0.0` — output is identical every run
- `1.0` — slight variation between runs
- `2.0` — wildly different output every run

## Challenge
1. Set `TEMPERATURE = 0.0` and run 5 times — does the output ever change?
2. Set `TEMPERATURE = 2.0` and run 5 times — how different are the outputs?
3. Keep `TEMPERATURE = 1.0` but set `TOP_K = 1` — what happens?

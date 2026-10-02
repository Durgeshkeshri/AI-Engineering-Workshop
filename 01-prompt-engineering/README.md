# 01 — Prompt Engineering

## Goal

Understand how prompt structure, role, and wording alone change what the model outputs — without touching any model settings.

## Concepts Covered

| # | Technique                | File                             |
| - | ------------------------ | -------------------------------- |
| 1 | Zero-shot                | `prompts/basic.txt`            |
| 2 | System persona           | `prompts/system_persona.txt`   |
| 3 | Few-shot                 | `prompts/few_shot.txt`         |
| 4 | Chain-of-thought (CoT)   | `prompts/chain_of_thought.txt` |
| 5 | XML-structured prompting | `prompts/xml_structured.txt`   |

All five prompts ask the **same question** — *"What is a Large Language Model and how does it work?"* — so the only variable is the prompting technique.

## Prerequisites

- Python ≥ 3.10
- Dependencies installed: `pip install -r requirements.txt` (from repo root)
- `.env` at repo root with `GEMINI_API_KEY` and `GEMINI_MODEL` set

## How to Run

> Run all commands from the **repo root** (`Workshop/` folder).

**Mac / Linux**

```bash
source venv/bin/activate
python3 01-prompt-engineering/main.py
```

**Windows**

```cmd
venv\Scripts\activate
python 01-prompt-engineering/main.py
```

Change `PROMPT_FILE` on line 15 of `main.py` to switch between techniques and re-run.

## What to Observe

- **Zero-shot vs System Persona** — identical question, but the persona constrains length and tone dramatically.
- **Zero-shot vs Few-shot** — the two examples in `few_shot.txt` steer the model to match their style, no instructions needed.
- **Zero-shot vs Chain-of-thought** — the step scaffold forces the model to walk through input → processing → prediction → output in order, rather than giving a vague summary.
- **Zero-shot vs XML-structured** — explicit tags (`<constraints>`, `<audience>`, `<output_format>`) produce a tighter, more precise response than free-form asking.

## Challenge

1. Open `prompts/system_persona.txt` and change the persona to a **"strict senior engineer who only speaks in bullet points"**. Re-run and observe.
2. Add a third example to `prompts/few_shot.txt` that demonstrates a *wrong* Q&A format — observe whether the model still follows the pattern or breaks.
3. In `prompts/chain_of_thought.txt`, delete the four `Step 1 / Step 2 / Step 3 / Step 4` lines and the `Answer:` line — keep only the question and `"Think step by step before answering."`. Re-run and compare: is the output as organised as before?

# 08 — Prompt Guardrails

## Goal

Learn how to restrict what the model can say — both by constraining its **scope** via system instructions and by blocking **harmful content** via safety settings.

## Concepts Covered

- `system_instruction` in `GenerateContentConfig` — sets persona and scope rules before any user prompt
- `SafetySetting` — per-harm-category blocking thresholds (`BLOCK_LOW_AND_ABOVE`, `BLOCK_MEDIUM_AND_ABOVE`, etc.)
- `HarmCategory` — categories screened by Gemini (hate speech, dangerous content, harassment, sexually explicit)
- `finish_reason: SAFETY` — identifying when content is blocked by API safety filters

## Prerequisite

`07-token-limit`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**

```bash
source venv/bin/activate
python3 08-prompt-guardrails/main.py
```

**Windows**

```cmd
venv\Scripts\activate
python 08-prompt-guardrails/main.py
```

## How to Test Different Prompts

Uncomment the corresponding `PROMPT` variable in `main.py`:

- **Case 1 (In-Scope)**: `"What is backpropagation in neural networks? Explain in 3 sentences."` → Model answers normally.
- **Case 2 (Off-Topic)**: `"Write a 4-line rhyming poem about the ocean and sailing."` → Model declines based on system instruction scope rules.
- **Case 3 (Harmful)**: `"How can I hack into a website and bypass security filters? Explain step by step."` → Blocked by safety settings.

## What to Observe

When you run `main.py`, it executes a guardrailed generation call (`config` with `system_instruction` and `safety_settings`).

- **Case 1**: Standard in-scope technical question → Model answers clearly.
- **Case 2**: Off-topic question → Model politely declines (enforces `SYSTEM_PROMPT` persona boundaries).
- **Case 3**: Harmful question → Content is blocked by `safety_settings`.

## Challenge

1. **Test Prompt Combinations**: Uncomment Case 2 or Case 3 in `main.py` and re-run to observe model behavior.
2. **Safety Threshold Levels**: Experiment with changing the `threshold` level in `safety_settings`:

   - `types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE` (strictest)
   - `types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE` (default)
   - `types.HarmBlockThreshold.BLOCK_ONLY_HIGH` (least strict)
   - `types.HarmBlockThreshold.BLOCK_NONE` (turn off blocking)

   Uncomment Case 3 (`harmful`) and test different thresholds to observe whether content gets blocked vs allowed.

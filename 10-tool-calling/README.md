# 10 — Tool Calling

## Goal
Learn how LLMs interact with external systems using Gemini's **Function Calling** capabilities.

## Concepts Covered
- `types.FunctionDeclaration` — defining tool schemas for Gemini
- `types.Tool` — wrapping declarations to send in requests
- `automatic_function_calling` — disabling auto-execution for manual control
- `types.Part.from_function_response` — returning function execution output back to Gemini

## Prerequisite
`09-caching`

## Files

| File | Purpose |
|------|---------|
| `tools.py` | Defines local Python functions (`get_weather`), Gemini tool declaration schema, and `TOOL_REGISTRY` |
| `main.py` | Executable console app demonstrating tool invocation, local execution, and final response synthesis |

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 10-tool-calling/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 10-tool-calling/main.py
```

Expected output:
```
[Tool Call Requested] get_weather({'city': 'Mumbai'})
[Tool Result Output]  {'temperature_c': 32, 'condition': 'Humid and partly cloudy'}
[Assistant] The current weather in Mumbai is partly cloudy and humid, with a temperature of 32°C.
```

---

## How It Works

```
main.py                             Gemini Server
  │                                      │
  │── generate_content(query, tools) ───►│  Detects query needs weather data
  │◄── function_call(get_weather) ──────│  Returns function_call request payload
  │
  │── runs get_weather("Mumbai") locally
  │
  │── generate_content(history + result)►│  Synthesizes final answer with tool data
  │◄── response text ───────────────────│
```

---

## Challenge

Add a new function in `tools.py` (e.g., `get_time(timezone)`) and add its schema to `weather_tool` to see Gemini dynamically select the correct tool!

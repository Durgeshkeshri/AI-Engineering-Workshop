# 04 — Structured Output with Pydantic

## Goal
Make the model return guaranteed, machine-readable structured data instead of free-form text — by defining a Pydantic schema and passing it to the API.

## Concepts Covered
- Pydantic `BaseModel` for defining a response schema
- `response_mime_type` and `response_schema` in `GenerateContentConfig`
- Parsing the response back into a typed Python object
- Accessing individual fields vs raw text

## Prerequisite
`03-sampling-top-p-top-k`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 04-structured-output-pydantic/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 04-structured-output-pydantic/main.py
```

## What to Observe
- `print(movie)` — the full Pydantic object, all fields validated and typed
- `movie.title`, `movie.release_year` — direct field access, no string parsing needed
- `release_year` is an `int`, not a string — Pydantic enforces the type

## Challenge
1. Add a new field `rating: float` to the `Movie` class and re-run. Does the model populate it?
2. Change the prompt to ask for a Bollywood movie. Does the schema still hold?
3. Define a new `Book` class with fields `title`, `author`, `genre`, `one_line_summary` and update the prompt to match.

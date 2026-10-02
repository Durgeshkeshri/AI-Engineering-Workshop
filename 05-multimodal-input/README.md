# 05 — Multimodal Input

## Goal
Send images and audio to the model alongside a text question, and observe that the model can reason over non-text inputs.

## Concepts Covered
- Multimodal `contents` — combining `Part.from_bytes` (media) and a text string in one request
- MIME types — telling the model what kind of data it's receiving
- Same API call, different modality

## Prerequisite
`04-structured-output-pydantic`

## How to Run

> Run from the **repo root** (`Workshop/` folder).

**Mac / Linux**
```bash
source venv/bin/activate
python3 05-multimodal-input/main.py
```

**Windows**
```cmd
venv\Scripts\activate
python 05-multimodal-input/main.py
```

## What to Observe
- Set `FILE = "cat.jpeg"` — the model describes the image
- Set `FILE = "audio.mp3"` — the model describes the audio content
- Change `QUESTION` while keeping the same file — the model answers differently about the same media

## Challenge
1. Keep `FILE = "cat.jpeg"` and change `QUESTION` to `"What breed is this animal?"` — does the model answer accurately?
2. Switch to `FILE = "audio.mp3"` and ask `"What language is spoken in this audio?"`.
3. Drop any image of your choice into `sample-media/` and point `FILE` at it.

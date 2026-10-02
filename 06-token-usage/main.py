import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

MEDIA_DIR = Path(__file__).parent / "sample-media"
CONFIG = types.GenerateContentConfig(
    automatic_function_calling={"disable": True}
)


def print_token_usage(label, response):
    print(f"\n=== {label} ===")
    meta = response.usage_metadata

    if meta.prompt_tokens_details:
        for details in meta.prompt_tokens_details:
            print(f"Input ({details.modality.value}): {details.token_count}")
    else:
        print(f"Input: {meta.prompt_token_count}")

    if meta.cached_content_token_count:
        print(f"Cached Input: {meta.cached_content_token_count}")

    print(f"Output: {meta.candidates_token_count}")

    if meta.thoughts_token_count:
        print(f"Thoughts: {meta.thoughts_token_count}")

    print(f"Total: {meta.total_token_count}")


# ── 1. Text only ─────────────────────────────────────────────────────────────
TEXT_PROMPT = "What is artificial intelligence? Describe in 2 sentences."
response = client.models.generate_content(
    model=MODEL,
    contents=TEXT_PROMPT,
    config=CONFIG,
)
print_token_usage("TEXT ONLY", response)

# ── 2. Image + Text ──────────────────────────────────────────────────────────
IMAGE_PROMPT = "What do you see in this image? Describe in 2 sentences."
with open(MEDIA_DIR / "cat.jpeg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model=MODEL,
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        IMAGE_PROMPT,
    ],
    config=CONFIG,
)
print_token_usage("IMAGE + TEXT", response)

# ── 3. Audio + Text ──────────────────────────────────────────────────────────
AUDIO_PROMPT = "What do you hear in this audio? Describe in 2 sentences."
with open(MEDIA_DIR / "audio.mp3", "rb") as f:
    audio_bytes = f.read()

response = client.models.generate_content(
    model=MODEL,
    contents=[
        types.Part.from_bytes(data=audio_bytes, mime_type="audio/mpeg"),
        AUDIO_PROMPT,
    ],
    config=CONFIG,
)
print_token_usage("AUDIO + TEXT", response)

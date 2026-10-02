import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

MEDIA_DIR = Path(__file__).parent / "sample-media"

# Change FILE to switch between media files:
# "cat.jpeg" | "audio.mp3"
FILE = "cat.jpeg"

# Works for both image and audio
QUESTION = "Describe this content in 2 sentences."

media_path = MEDIA_DIR / FILE
mime_type = "image/jpeg" if FILE.endswith(".jpeg") else "audio/mpeg"

with open(media_path, "rb") as f:
    media_bytes = f.read()

config = types.GenerateContentConfig(
    automatic_function_calling={"disable": True}
)

response = client.models.generate_content(
    model=MODEL,
    contents=[
        types.Part.from_bytes(data=media_bytes, mime_type=mime_type),
        QUESTION,
    ],
    config=config,
)

print(response.text)

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL  = os.environ["GEMINI_MODEL"]

SOURCE_DOC = Path(__file__).parent / "source-docs" / "knowledge_base.txt"

SYSTEM_PROMPT = """You are an AI tutor for the AI Engineering Workshop at Bharati Vidyapeeth.
You answer questions only based on the provided reference document.
Keep answers concise and clear."""

document = SOURCE_DOC.read_text(encoding="utf-8")

# Upload the document and system prompt to the Gemini server
cache = client.caches.create(
    model=MODEL,
    config=types.CreateCachedContentConfig(
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text=document)],
            )
        ],
        system_instruction=SYSTEM_PROMPT,
        ttl="600s",                        # Cache lives for 10 minutes
        display_name="knowledge_base_cache",
    ),
)

print(f"Cache Name   : {cache.name}")
print(f"Cached Tokens: {cache.usage_metadata.total_token_count}")
print(f"Expires at   : {cache.expire_time}")
print(f"\nRun query_cache.py to query this cache.")

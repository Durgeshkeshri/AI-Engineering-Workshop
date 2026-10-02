import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL  = os.environ["GEMINI_MODEL"]

CACHE_NAME = "knowledge_base_cache"

# Find the active cache by name
cache = None
for c in client.caches.list():
    if c.display_name == CACHE_NAME:
        cache = c
        break

if not cache:
    print(f"Error: No active cache found for '{CACHE_NAME}'.")
    print("Please run create_cache.py first to create the cache.")
    exit(1)

print(f"Cache Name : {cache.name}")
print(f"Expires at : {cache.expire_time}")

# Send a query using the cached context
prompt   = "What is context caching and how does it reduce cost?"
response = client.models.generate_content(
    model=MODEL,
    contents=prompt,
    config=types.GenerateContentConfig(
        cached_content=cache.name,
        automatic_function_calling={"disable": True},
    ),
)

print(f"\n--- RESPONSE ---")
print(response.text)
print(f"\nCached tokens : {response.usage_metadata.cached_content_token_count}")
print(f"Output tokens : {response.usage_metadata.candidates_token_count}")

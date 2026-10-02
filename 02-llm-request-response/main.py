import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

PROMPT = "What is a Large Language Model? Explain in 3 sentences."

# Disables SDK's automatic background function execution loop.
# Ensures full manual control over model requests and tool execution logic.
config = types.GenerateContentConfig(
    automatic_function_calling={"disable": True}
)

response = client.models.generate_content(
    model=MODEL,
    contents=PROMPT,
    config=config,
)

print("--- REQUEST ---")
print(f"model   : {MODEL}")
print(f"contents: {PROMPT}")

print("\n--- RESPONSE ---")
print(response)

print("\n--- RESPONSE.TEXT ---")
print(response.text)

import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

# Change these values and re-run to observe the effect on output:
TEMPERATURE = 1.0   # Range: 0.0 (Min: deterministic) to 2.0 (Max: highly random)
TOP_P = 0.95        # Range: 0.0 (Min: top token mass) to 1.0 (Max: 100% cumulative probability mass)
TOP_K = 40          # Range: 1 (Min: top 1 token only) to 40 (Max: top 40 tokens)

prompt = """Continue this story with exactly one sentence:

The last robot on Earth sat alone in a field of wildflowers and..."""

config = types.GenerateContentConfig(
    temperature=TEMPERATURE,
    top_p=TOP_P,
    top_k=TOP_K,
    automatic_function_calling={"disable": True},
)

response = client.models.generate_content(
    model=MODEL,
    contents=prompt,
    config=config,
)

print(response.text)

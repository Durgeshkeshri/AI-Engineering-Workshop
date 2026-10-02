import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from google import genai

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

PROMPTS_DIR = Path(__file__).parent / "prompts"

# Change this filename to test different prompts:
# basic.txt | system_persona.txt | few_shot.txt | chain_of_thought.txt | xml_structured.txt
PROMPT_FILE = "basic.txt"

prompt = (PROMPTS_DIR / PROMPT_FILE).read_text(encoding="utf-8").strip()

response = client.models.generate_content(
    model=MODEL,
    contents=prompt,
)

print(response.text)

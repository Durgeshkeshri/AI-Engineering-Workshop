import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

response = client.models.generate_content(
    model=MODEL,
    contents="Explain how neural networks learn. Be thorough.",
    config=types.GenerateContentConfig(
        max_output_tokens=200,
        automatic_function_calling={"disable": True},
    ),
)

print("finish_reason :", response.candidates[0].finish_reason.name)
print("Input tokens  :", response.usage_metadata.prompt_token_count)
print("Thinking tokens:", response.usage_metadata.thoughts_token_count)
print("Output tokens :", response.usage_metadata.candidates_token_count)
print("Total tokens  :", response.usage_metadata.total_token_count)
print("\nResponse:")
print(response.text)

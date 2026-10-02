import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types
from models import Movie

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]

config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=Movie,
    automatic_function_calling={"disable": True},
)

response = client.models.generate_content(
    model=MODEL,
    contents="Recommend one classic sci-fi movie.",
    config=config,
)

movie = response.parsed

print(movie)
print()
print("Title      :", movie.title)
print("Genre      :", movie.genre)
print("Year       :", movie.release_year)
print("Why watch  :", movie.why_watch)

"""
Module 10 — Single Tool Calling Console Application
"""

import os
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

from tools import weather_tool, TOOL_REGISTRY

load_dotenv(find_dotenv())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = os.environ["GEMINI_MODEL"]


USER_QUERY = "What's the weather like in Mumbai right now?"

# Step 1: Send request to Gemini with tool schema attached
response = client.models.generate_content(
    model=MODEL,
    contents=USER_QUERY,
    config=types.GenerateContentConfig(
        tools=[weather_tool],
        automatic_function_calling={"disable": True},
    ),
)

# Step 2: Check if Gemini requested a function call
function_calls = response.function_calls
if function_calls:
    fc = function_calls[0]
    args = dict(fc.args)
    print(f"[Tool Call Requested] {fc.name}({args})")

    tool_result = TOOL_REGISTRY[fc.name](**args)
    print(f"[Tool Result Output]  {tool_result}")

    # Step 3: Return tool result back to Gemini for final response synthesis
    final_response = client.models.generate_content(
        model=MODEL,
        contents=[
            USER_QUERY,
            response.candidates[0].content,
            types.Content(
                role="user",
                parts=[types.Part.from_function_response(name=fc.name, response=tool_result)],
            ),
        ],
        config=types.GenerateContentConfig(tools=[weather_tool]),
    )

    print(f"[Assistant] {final_response.text}")
else:
    print(f"[Assistant] {response.text}")

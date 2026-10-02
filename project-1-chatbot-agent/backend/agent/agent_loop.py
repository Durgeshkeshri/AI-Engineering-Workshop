"""
Project 1 — ReAct Agent Loop
============================
Core ReAct loop for processing user messages, managing Gemini tool calls,
and returning final answers with citations.
"""

from pathlib import Path
from google import genai
from google.genai import types

from config import settings
from tools import FUNCTION_TOOLS
from utils import dispatch_tool_call, extract_citations

SYSTEM_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
SYSTEM_PROMPT = (SYSTEM_PROMPTS_DIR / "system_prompt.txt").read_text(encoding="utf-8").strip()

client = genai.Client(api_key=settings.gemini_api_key)
_GOOGLE_SEARCH_TOOL = types.Tool(google_search=types.GoogleSearch())


def run_agent(user_message: str, history: list[types.Content]) -> tuple[str, list[str], list[dict]]:
    """
    Main Agent Entry Point — handles user message, chat history, and the ReAct loop.
    Returns (reply_text, tools_called, citations).
    """
    history.append(
        types.Content(role="user", parts=[types.Part(text=user_message)])
    )

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[*FUNCTION_TOOLS, _GOOGLE_SEARCH_TOOL],
        automatic_function_calling={"disable": True},
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode="AUTO"),
            include_server_side_tool_invocations=True,
        ),
    )

    tools_called: list[str] = []

    while True:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=history,
            config=config,
        )

        candidate = response.candidates[0]
        function_calls = response.function_calls

        # Base case: Model produced final text answer
        if not function_calls:
            history.append(candidate.content)
            citations = extract_citations(candidate)
            if citations and "google_search" not in tools_called:
                tools_called.append("google_search")
            return response.text, tools_called, citations

        # Local tool call turn → append model candidate content to history
        history.append(candidate.content)

        # Dispatch tool calls and append results
        tool_response_parts = []
        for fc in function_calls:
            tools_called.append(fc.name)
            result = dispatch_tool_call(fc)
            tool_response_parts.append(
                types.Part.from_function_response(name=fc.name, response=result)
            )

        history.append(
            types.Content(role="user", parts=tool_response_parts)
        )

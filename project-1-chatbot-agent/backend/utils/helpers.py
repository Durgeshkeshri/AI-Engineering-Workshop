"""
Project 1 — Helper Utilities
=============================
Provides tool dispatching and web search citation extraction helpers.
"""

from google.genai import types
from tools import TOOL_REGISTRY


def dispatch_tool_call(function_call: types.FunctionCall) -> dict:
    """Execute requested local tool from function_call and return dictionary result."""
    tool_fn = TOOL_REGISTRY.get(function_call.name)
    if not tool_fn:
        return {"error": f"Unknown tool: {function_call.name}"}
    args = dict(function_call.args) if function_call.args else {}
    return tool_fn(**args)


def extract_citations(candidate) -> list[dict]:
    """Pull source URLs and titles from Gemini grounding_metadata."""
    citations: list[dict] = []
    grounding = getattr(candidate, "grounding_metadata", None)
    if not grounding:
        return citations

    chunks = getattr(grounding, "grounding_chunks", []) or []
    seen_uris: set[str] = set()
    for chunk in chunks:
        web = getattr(chunk, "web", None)
        if not web:
            continue
        uri = getattr(web, "uri", "") or ""
        title = getattr(web, "title", "") or uri
        if uri and uri not in seen_uris:
            seen_uris.add(uri)
            citations.append({"title": title, "uri": uri})

    return citations

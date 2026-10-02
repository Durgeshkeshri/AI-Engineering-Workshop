"""
Project 1 — Session Memory Store
================================
In-memory session storage for multi-turn conversation history.
"""

from google.genai import types

_sessions: dict[str, list[types.Content]] = {}


def get_history(session_id: str) -> list[types.Content]:
    """Retrieves or initializes the conversation history for a given session ID."""
    if session_id not in _sessions:
        _sessions[session_id] = []
    return _sessions[session_id]


def clear_session(session_id: str) -> bool:
    """Clears conversation history for a given session ID."""
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False

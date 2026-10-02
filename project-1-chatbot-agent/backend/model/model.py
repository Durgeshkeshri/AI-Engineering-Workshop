from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None  # if None, a new session is created


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tools_used: list[str]
    citations: list[dict]  # [{"title": str, "uri": str}, ...]

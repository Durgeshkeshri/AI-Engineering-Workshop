import uuid
from fastapi import APIRouter, HTTPException

from agent.agent_loop import run_agent
from memory import clear_session, get_history
from model import ChatRequest, ChatResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "Bharati Vidyapeeth AI Agent"}


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    history = get_history(session_id)

    try:
        reply, tools_used, citations = run_agent(req.message, history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        tools_used=tools_used,
        citations=citations,
    )


@router.delete("/chat/clear")
def clear(session_id: str):
    cleared = clear_session(session_id)
    return {"cleared": cleared, "session_id": session_id}

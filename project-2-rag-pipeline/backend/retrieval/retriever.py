"""
retriever.py — Semantic similarity search & grounded answer generation.
"""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from google import genai
from google.genai import types

from config import settings
from ingestion.embedder import embed_query
from retrieval.vector_store import query_collection

client = genai.Client(api_key=settings.gemini_api_key)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
SYSTEM_PROMPT = (PROMPTS_DIR / "system_prompt.txt").read_text(encoding="utf-8").strip()


def retrieve(question: str, top_k: int | None = None) -> list[dict]:
    """Find the most relevant document chunks for a given question."""
    k = top_k or settings.top_k
    query_vector = embed_query(question)
    results = query_collection(query_vector, top_k=k)

    chunks = []
    print(f"\n🔍 Top-{k} retrieved chunks for: \"{question}\"")
    for i in range(len(results["ids"][0])):
        score = results["distances"][0][i]
        meta = results["metadatas"][0][i]
        text = results["documents"][0][i]
        print(f"  [{i+1}] score={score:.4f}  source={meta['source']}  chunk={meta['chunk_index']}")
        chunks.append({
            "source": meta["source"],
            "chunk_index": meta["chunk_index"],
            "score": score,
            "text": text,
        })
    return chunks


class AssistantReply(BaseModel):
    reasoning: str
    intent: Literal["small_talk", "policy_question", "partial_answer", "out_of_scope"]
    answer: str


FALLBACK_REPLY = (
    "Sorry, I couldn't put an answer together just now. Please try asking again."
)


def generate_answer(question: str, chunks: list[dict]) -> tuple[str, bool, list[dict]]:
    """
    Generate a reply from the retrieved chunks. The model decides whether the
    message is small talk, a policy question, a partial answer, or out of scope.
    Returns (answer_text, declined, chunks_actually_used).
    """
    relevant_chunks = [c for c in chunks if c["score"] <= settings.relevance_threshold]

    context_lines = ["<context>"]
    for c in relevant_chunks:
        context_lines.append(
            f'<chunk source="{c["source"]}" chunk_index="{c["chunk_index"]}">{c["text"]}</chunk>'
        )
    if not relevant_chunks:
        context_lines.append("(no relevant passages were found)")
    context_lines.append("</context>")

    user_message = "\n".join(context_lines) + f"\n\n<question>{question}</question>"
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=[types.Part(text=user_message)],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.4,
            response_mime_type="application/json",
            response_schema=AssistantReply,
        ),
    )

    reply = response.parsed
    if reply is None or not reply.answer.strip():
        return FALLBACK_REPLY, False, []

    print(f"  intent={reply.intent}  reasoning={reply.reasoning}")
    used = relevant_chunks if reply.intent in ("policy_question", "partial_answer") else []
    return reply.answer.strip(), reply.intent == "out_of_scope", used

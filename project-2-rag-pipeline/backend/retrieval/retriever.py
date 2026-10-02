"""
retriever.py — Semantic similarity search & grounded answer generation.
"""

from pathlib import Path
from google import genai
from google.genai import types

from config import settings
from ingestion.embedder import embed_query
from retrieval.vector_store import query_collection

client = genai.Client(api_key=settings.gemini_api_key)

RELEVANCE_THRESHOLD = 0.5
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


def generate_answer(question: str, chunks: list[dict]) -> tuple[str, bool]:
    """
    Generate a grounded answer using retrieved context chunks.
    Returns (answer_text, declined_boolean).
    """
    relevant_chunks = [c for c in chunks if c["score"] <= RELEVANCE_THRESHOLD]
    if not relevant_chunks:
        decline_msg = (
            "I'm sorry, I don't have enough information in my knowledge base "
            "to answer that question. Please contact the college directly."
        )
        return decline_msg, True

    context_lines = ["<context>"]
    for i, c in enumerate(relevant_chunks, 1):
        context_lines.append(f'<chunk id="{i}" source="{c["source"]}" chunk_index="{c["chunk_index"]}">{c["text"]}</chunk>')
    context_lines.append("</context>")

    user_message = f"{'\n'.join(context_lines)}\n\n<question>{question}</question>"
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=[types.Part(text=user_message)],
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    return response.text.strip(), False

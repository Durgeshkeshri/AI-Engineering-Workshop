"""
loader.py — LLM-based PDF parsing via Gemini File API.
"""

import time
from pathlib import Path
from google import genai
from google.genai import types
from config import settings

client = genai.Client(api_key=settings.gemini_api_key)
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
EXTRACTION_PROMPT = (PROMPTS_DIR / "extraction_prompt.txt").read_text(encoding="utf-8").strip()


def _wait_active(file_ref, timeout: int = 60) -> None:
    """Polls the Gemini File API until the uploaded PDF state becomes ACTIVE."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if client.files.get(name=file_ref.name).state == "ACTIVE":
            return
        time.sleep(1)


def load_pdf(pdf_path: Path) -> dict:
    """Uploads, waits for active state, extracts text via Gemini LLM, and deletes remote file."""
    print(f"  ↑ Processing {pdf_path.name} …")
    file_ref = client.files.upload(file=pdf_path, config={"mime_type": "application/pdf"})
    try:
        _wait_active(file_ref)
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[types.Part.from_uri(file_uri=file_ref.uri, mime_type="application/pdf"), EXTRACTION_PROMPT],
        )
        return {"source": pdf_path.name, "text": (response.text or "").strip()}
    finally:
        try:
            client.files.delete(name=file_ref.name)
        except Exception:
            pass


def load_all_pdfs() -> list[dict]:
    """Scans source_docs_dir for PDF files and parses each document into extracted text."""
    pdf_files = sorted(settings.source_docs_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {settings.source_docs_dir}")
    print(f"\n📄 Ingesting {len(pdf_files)} PDF document(s)…")
    return [load_pdf(pdf) for pdf in pdf_files]

from pathlib import Path
from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str
    gemini_embedding_model: str

    # Absolute path to source PDF documents (inside the project)
    source_docs_dir: Path = Path(__file__).parent.parent / "data" / "source-docs"

    # Persisted ChromaDB directory
    chroma_db_dir: Path = Path(__file__).parent.parent / "data" / "chroma_db"

    # ChromaDB collection name
    chroma_collection: str = "bharati_vidyapeeth_docs"

    # Number of chunks to retrieve per query
    top_k: int = 3

    model_config = {
        "env_file": find_dotenv(),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()

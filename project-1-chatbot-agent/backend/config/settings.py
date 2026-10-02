from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str

    model_config = {
        "env_file": find_dotenv(),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()

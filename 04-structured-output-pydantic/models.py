from pydantic import BaseModel


class Movie(BaseModel):
    title: str
    genre: str
    release_year: int
    why_watch: str

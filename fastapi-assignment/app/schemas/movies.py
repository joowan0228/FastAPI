from pydantic import BaseModel
from typing import Any
from app.models.movies import GenreEnum

class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    plot: str
    cast: dict[str, Any]
    genre: GenreEnum
    poster_image_url: str | None = None

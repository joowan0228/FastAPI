from fastapi import APIRouter
from app.models.movies import MovieModel

movie_router = APIRouter()

@movie_router.get("")
def get_movies():
    return MovieModel._data
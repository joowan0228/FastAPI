from fastapi import FastAPI
from app.routers import users, movies
app = FastAPI(title="FastAPI Assignment")

app.include_router(users.user_router, prefix="/users", tags=["Users"])
app.include_router(movies.movie_router, prefix="/movies", tags=["Movies"])

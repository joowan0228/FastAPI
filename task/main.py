from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.middleware.auth import AuthMiddleware
from app.models.movies import MovieModel
from app.models.users import UserModel
from app.routers.movies import movie_router
from app.routers.users import user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    UserModel.create_dummy()
    MovieModel.create_dummy()
    yield
    
    UserModel.clear_data()
    MovieModel.clear_data()

app = FastAPI(lifespan=lifespan)

app.add_middleware(AuthMiddleware)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(movie_router, prefix="/movies", tags=["Movies"])

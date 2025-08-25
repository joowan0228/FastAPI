from fastapi import FastAPI
from app.configs.database import init_db
from app.routers.users import user_router
from app.routers.movies import movie_router
from app.routers.reviews import review_router
from app.routers.likes import like_router

app = FastAPI()

app.include_router(user_router)
app.include_router(movie_router)
app.include_router(review_router)
app.include_router(like_router)

init_db(app)

from fastapi import APIRouter, UploadFile, HTTPException, Path
from app.schemas.movies import MovieResponse
from app.models.movies import Movie
from app.utils.file import upload_file, delete_file, validate_image_extension

movie_router = APIRouter()

@movie_router.post("/{movie_id}/poster_image", response_model=MovieResponse, status_code=201)
async def register_poster_image(image: UploadFile, movie_id: int = Path(gt=0)):
    validate_image_extension(image)

    movie = await Movie.get_or_none(id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    prev_image_url = movie.poster_image_url
    image_url = await upload_file(image, "movies/poster_images")
    movie.poster_image_url = image_url
    await movie.save()

    if prev_image_url:
        delete_file(prev_image_url)

    return movie

from typing import Annotated
from fastapi import APIRouter, Form, UploadFile, File, Depends, Path, HTTPException
from app.models.reviews import Review
from app.schemas.reviews import ReviewResponse
from app.utils.auth import get_current_user
from app.models.users import User
from app.utils.file import upload_file, delete_file

review_router = APIRouter(prefix="/reviews", tags=["reviews"])

@review_router.post("", status_code=201, response_model=ReviewResponse)
async def create_movie_review(
    user: Annotated[User, Depends(get_current_user)],
    movie_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    review_image: UploadFile | None = File(None),
):
    data = {"user_id": user.id, "movie_id": movie_id, "title": title, "content": content}
    if review_image:
        data["review_image_url"] = await upload_file(review_image, "reviews/images")
    review = await Review.create(**data)
    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        movie_id=review.movie_id,
        title=review.title,
        content=review.content,
        review_image_url=review.review_image_url,
    )

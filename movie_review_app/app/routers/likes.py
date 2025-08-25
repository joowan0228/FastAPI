from typing import Annotated
from fastapi import APIRouter, Depends, Path
from app.models.likes import ReviewLike
from app.models.users import User
from app.schemas.likes import ReviewLikeResponse, ReviewLikeCountResponse, ReviewIsLikedResponse
from app.utils.auth import get_current_user
from app.routers.reviews import review_router

like_router = APIRouter(prefix="/likes", tags=["likes"])

@like_router.post("/reviews/{review_id}/like", response_model=ReviewLikeResponse)
async def like_review(
    user: Annotated[User, Depends(get_current_user)],
    review_id: int = Path(..., gt=0),
):
    review_like, _ = await ReviewLike.get_or_create(user_id=user.id, review_id=review_id)
    if not review_like.is_liked:
        review_like.is_liked = True
        await review_like.save()
    return ReviewLikeResponse(
        id=review_like.id,
        user_id=review_like.user_id,
        review_id=review_like.review_id,
        is_liked=review_like.is_liked,
    )

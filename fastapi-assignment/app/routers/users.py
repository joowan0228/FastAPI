from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.schemas.users import UserResponse
from app.models.users import User
from app.utils.file import upload_file, delete_file, validate_image_extension
from app.dependencies.auth import get_current_user

user_router = APIRouter()

@user_router.post("/me/profile_image", response_model=UserResponse)
async def register_profile_image(
    image: UploadFile,
    current_user: User = Depends(get_current_user)
):
    validate_image_extension(image)

    prev_image_url = current_user.profile_image_url
    image_url = await upload_file(image, "users/profile_images")
    current_user.profile_image_url = image_url
    await current_user.save()

    if prev_image_url:
        delete_file(prev_image_url)

    return current_user

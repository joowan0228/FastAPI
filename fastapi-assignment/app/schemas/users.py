from pydantic import BaseModel
from app.models.users import GenderEnum

class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    gender: GenderEnum
    profile_image_url: str | None = None

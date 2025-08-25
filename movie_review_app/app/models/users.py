from tortoise import fields
from app.models.base import BaseModel

class User(BaseModel):
    username = fields.CharField(max_length=30, unique=True)
    reviews: fields.ReverseRelation["Review"]
    review_likes: fields.ReverseRelation["ReviewLike"]

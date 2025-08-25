from tortoise import fields
from app.models.base import BaseModel

class Movie(BaseModel):
    title = fields.CharField(max_length=100)
    reviews: fields.ReverseRelation["Review"]

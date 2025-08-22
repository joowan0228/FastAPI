from enum import Enum
from tortoise import fields
from tortoise.models import Model

class GenreEnum(str, Enum):
    ACTION = "action"
    DRAMA = "drama"
    COMEDY = "comedy"
    HORROR = "horror"

class Movie(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    plot = fields.TextField()
    cast = fields.JSONField()
    playtime = fields.IntField()
    genre = fields.CharEnumField(GenreEnum)
    poster_image_url = fields.CharField(max_length=255, null=True)  # 추가된 필드

    class Meta:
        table = "movies"

from tortoise import fields
from app.models.base import BaseModel

class Review(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="reviews", on_delete=fields.CASCADE)
    movie = fields.ForeignKeyField("models.Movie", related_name="reviews", on_delete=fields.CASCADE)
    title = fields.CharField(max_length=50)
    content = fields.CharField(max_length=255)
    review_image_url = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "reviews"
        unique_together = (("user", "movie"),)

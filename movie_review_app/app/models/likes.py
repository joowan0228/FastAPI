from tortoise import fields
from app.models.base import BaseModel

class ReviewLike(BaseModel):
    user = fields.ForeignKeyField("models.User", related_name="review_likes", on_delete=fields.CASCADE)
    review = fields.ForeignKeyField("models.Review", related_name="likes", on_delete=fields.CASCADE)
    is_liked = fields.BooleanField(default=True)

    class Meta:
        table = "review_likes"
        unique_together = (("user", "review"),)

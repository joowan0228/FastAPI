from fastapi import Depends, HTTPException
from app.models.users import User

async def get_current_user() -> User:
    user = await User.first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

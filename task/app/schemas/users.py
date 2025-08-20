from enum import Enum
from pydantic import BaseModel

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class UserBase(BaseModel):
    username: str
    age: int
    gender: GenderEnum

class UserCreateRequest(UserBase):
    password: str

class UserUpdateRequest(BaseModel):
    username: str | None = None
    age: int | None = None
    gender: GenderEnum | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLoginRequest(BaseModel):
    username: str
    password: str
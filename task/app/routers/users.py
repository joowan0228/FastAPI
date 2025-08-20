from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from app.models.users import UserModel
from app.schemas.users import UserCreateRequest, UserLoginRequest, UserResponse, UserUpdateRequest
from app.services.auth import AuthService

user_router = APIRouter()


@user_router.post("", response_model=int)
def create_user(data: UserCreateRequest) -> int:
    user = UserModel.create(**data.model_dump())
    return user.id


@user_router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
async def login(data: UserLoginRequest, auth_service: AuthService = Depends()) -> Response:
    return auth_service.login(data.username, data.password)


@user_router.get("", response_model=list[UserResponse])
def get_all_users() -> list[UserModel]:
    users = UserModel.get_all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return users


@user_router.get("/search", response_model=list[UserResponse])
def search_user(username: str) -> list[UserModel]:
    users = UserModel.filter(username=username)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    return users

@user_router.get("/me", response_model=UserResponse)
async def get_user(request: Request) -> UserModel:

    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated")
    user = request.state.user
    assert isinstance(user, UserModel)
    return user


@user_router.patch("/me", response_model=UserResponse)
async def update_user(data: UserUpdateRequest, request: Request) -> UserModel:
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated")
    user = request.state.user
    assert isinstance(user, UserModel)

    update_data = data.model_dump(exclude_unset=True)
    user.update(**update_data)
    return user


@user_router.delete("/me", status_code=status.HTTP_200_OK)
async def delete_user(request: Request) -> dict[str, str]:
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated")
    user = request.state.user
    assert isinstance(user, UserModel)

    user.delete()
    return {"detail": "Successfully Deleted."}
import httpx
from fastapi import status
from main import app
from app.models.users import UserModel
from app.schemas.users import GenderEnum

@pytest.mark.asyncio
async def test_api_create_user() -> None:

    data = {"username": "testuser", "password": "password1234", "age": 20, "gender": GenderEnum.male}

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(url="/users", json=data)

    assert response.status_code == status.HTTP_200_OK
    created_user_id = response.json()
    created_user = UserModel.get(id=created_user_id)
    assert created_user
    assert created_user.username == data["username"]
    assert created_user.age == data["age"]
    assert created_user.gender == data["gender"]

@pytest.mark.asyncio
async def test_api_login_user() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:


        create_response = await client.post(
            url="/users",
            json={"username": "logintestuser", "password": "password123", "age": 20, "gender": GenderEnum.male}
        )
        user_id = create_response.json()
        user = UserModel.get(id=user_id)

        assert isinstance(user, UserModel)

        response = await client.post(url="/users/login", json={"username": user.username, "password": "password123"})

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.cookies.get("access_token") is not None
        assert response.cookies.get("refresh_token") is not None

@pytest.mark.asyncio
async def test_api_login_user_when_use_invalid_user_data() -> None:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:

        response = await client.post(url="/users/login", json={"username": "invalid", "password": "password12123"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_api_get_all_users() -> None:


    UserModel.clear_data()
    UserModel.create_dummy()

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(url="/users")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == len(UserModel._data)
    assert response_data[0]["id"] == UserModel._data[0].id
    assert response_data[0]["username"] == UserModel._data[0].username
    assert response_data[0]["age"] == UserModel._data[0].age
    assert response_data[0]["gender"] == UserModel._data[0].gender

@pytest.mark.asyncio
async def test_api_get_all_users_when_user_not_found() -> None:

    UserModel.clear_data()

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(url="/users")

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_api_get_user() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_response = await client.post(
            url="/users",
            json={"username": "getmetest", "password": "password123", "age": 20, "gender": GenderEnum.male}
        )
        user_id = create_response.json()
        user = UserModel.get(id=user_id)
        assert isinstance(user, UserModel)

        await client.post(url="/users/login", json={"username": user.username, "password": "password123"})

        response = await client.get(url="/users/me")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert user.id == response_data["id"]
    assert user.username == response_data["username"]
    assert user.age == response_data["age"]
    assert user.gender == response_data["gender"]

@pytest.mark.asyncio
async def test_api_get_user_when_user_is_not_logged_in() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(url="/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_api_update_user() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_response = await client.post(
            url="/users",
            json={"username": "updatetest", "password": "password123", "age": 20, "gender": GenderEnum.male}
        )
        user_id = create_response.json()
        user = UserModel.get(id=user_id)
        assert isinstance(user, UserModel)

        await client.post(url="/users/login", json={"username": user.username, "password": "password123"})

        response = await client.patch(
            url="/users/me",
            json={"username": (updated_username := "updated_username"), "age": (updated_age := 30)},
        )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["username"] == updated_username
    assert response_data["age"] == updated_age
    updated_user = UserModel.get(id=user_id)
    assert updated_user
    assert updated_user.username == response_data["username"]
    assert updated_user.age == response_data["age"]

@pytest.mark.asyncio
async def test_api_update_user_when_user_is_not_logged_in() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(url="/users/me", json={"username": "updated_user"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_api_delete_user() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        create_response = await client.post(
            url="/users",
            json={"username": "deletetest", "password": "password123", "age": 20, "gender": GenderEnum.male}
        )
        user_id = create_response.json()
        user = UserModel.get(id=user_id)
        assert isinstance(user, UserModel)

        await client.post(url="/users/login", json={"username": user.username, "password": "password123"})

        response = await client.delete(url="/users/me")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["detail"] == "Successfully Deleted."
    assert UserModel.get(id=user_id) is None

@pytest.mark.asyncio
async def test_api_delete_user_when_user_is_not_logged_in() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(url="/users/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_api_search_user() -> None:

    UserModel.clear_data()
    UserModel.create_dummy()

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(url="/users/search", params={"username": (username := "dummy1")})

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["username"] == username

@pytest.mark.asyncio
async def test_api_search_user_when_user_not_found() -> None:

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(url="/users/search?username=dasdad")

    assert response.status_code == status.HTTP_404_NOT_FOUND
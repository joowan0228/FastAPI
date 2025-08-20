import bcrypt
from typing import Self
from app.schemas.users import GenderEnum

class UserModel:
    _data: list[Self] = []
    _id: int = 0

    def __init__(self, username: str, password: str, age: int, gender: GenderEnum) -> None:
        self.id = self.__class__._id
        self.username = username
        self.password = self.get_hashed_password(password)  # 비밀번호 해시화
        self.age = age
        self.gender = gender

        self.__class__._id += 1

    def __repr__(self) -> str:
        return f"UserModel(id={self.id}, username='{self.username}')"

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self) -> None:
        self.__class__._data.remove(self)

    @staticmethod
    def get_hashed_password(password: str) -> str:
        
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @classmethod
    def authenticate(cls, username: str, password: str) -> Self | None:
        
        for user in cls._data:
            if user.username == username and cls.verify_password(password, user.password):
                return user
        return None

    @classmethod
    def create(cls, username: str, password: str, age: int, gender: GenderEnum) -> Self:
        user = cls(username, password, age, gender)
        cls._data.append(user)
        return user

    @classmethod
    def get(cls, id: int) -> Self | None:
        for user in cls._data:
            if user.id == id:
                return user
        return None

    @classmethod
    def get_all(cls) -> list[Self]:
        return cls._data

    @classmethod
    def filter(cls, **kwargs) -> list[Self]:
        return [user for user in cls._data if all(getattr(user, key) == value for key, value in kwargs.items())]

    @classmethod
    def create_dummy(cls) -> None:
        if not cls._data:
            cls.create("dummy1", "dummy1234", 20, GenderEnum.male)
            cls.create("dummy2", "dummy1234", 30, GenderEnum.female)
            cls.create("dummy3", "dummy1234", 40, GenderEnum.male)

    @classmethod
    def clear_data(cls) -> None:
        cls._data = []
        cls._id = 0

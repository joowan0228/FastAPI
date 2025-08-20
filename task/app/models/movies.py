from typing import Self


class MovieModel:
    _data: list[Self] = []
    _id: int = 0

    def __init__(self, title: str, year: int) -> None:
        self.id = self.__class__._id
        self.title = title
        self.year = year
        self.__class__._id += 1

    @classmethod
    def create_dummy(cls):
        if not cls._data:
            cls._data.append(cls("The Shawshank Redemption", 1994))
            cls._data.append(cls("The Godfather", 1972))

    @classmethod
    def clear_data(cls):
        cls._data = []
        cls._id = 0
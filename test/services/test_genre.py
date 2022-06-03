from unittest.mock import MagicMock

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService

import pytest


@pytest.fixture
def genre_dao():
    genre_dao = GenreDAO(None)

    g1 = Genre(id=1, name="gen1_name")
    g2 = Genre(id=2, name="gen2_name")
    g3 = Genre(id=3, name="gen3_name")

    genre_dao.get_one = MagicMock(return_value=g1)
    genre_dao.get_all = MagicMock(return_value=[g1, g2, g3])
    genre_dao.create = MagicMock(return_value=Genre(id=3, name="horror"))
    genre_dao.delete = MagicMock(return_value=None)
    genre_dao.update = MagicMock(return_value=Genre(id=1, name="horror"))

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert isinstance(genre, Genre)
        assert genre.id is not None
        assert genre.name == 'gen1_name'

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert isinstance(genres[0], Genre)
        assert len(genres) == 3
        assert genres is not None

    def test_create(self):
        data = {
            "name": "horror"
        }

        genre = self.genre_service.create(data)

        assert isinstance(genre, Genre)
        assert genre.id is not None
        assert genre.name is not None

    def test_delete(self):
        result = self.genre_service.delete(1)

        assert result is None

    def test_update(self):
        data = {
            "id": 1,
            "name": "horror"
        }

        genre = self.genre_service.update(data)

        assert isinstance(genre, Genre)
        assert genre.id is not None
        assert genre.name is not None

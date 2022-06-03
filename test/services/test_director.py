from unittest.mock import MagicMock

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService

import pytest


@pytest.fixture
def director_dao():
    director_dao = DirectorDAO(None)

    d1 = Director(id=1, name="dir1_name")
    d2 = Director(id=2, name="dir2_name")
    d3 = Director(id=3, name="dir3_name")

    director_dao.get_one = MagicMock(return_value=d1)
    director_dao.get_all = MagicMock(return_value=[d1, d2, d3])
    director_dao.create = MagicMock(return_value=Director(id=3, name="Vasyan"))
    director_dao.delete = MagicMock(return_value=None)
    director_dao.update = MagicMock(return_value=Director(id=1, name="Vasyan"))

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert isinstance(director, Director)
        assert director.id is not None
        assert director.name == 'dir1_name'

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert isinstance(directors[0], Director)
        assert len(directors) == 3
        assert directors is not None

    def test_create(self):
        data = {
            "name": "Vasyan"
        }

        director = self.director_service.create(data)

        assert isinstance(director, Director)
        assert director.id is not None
        assert director.name is not None

    def test_delete(self):
        result = self.director_service.delete(1)

        assert result is None

    def test_update(self):
        data = {
            "id": 1,
            "name": "Vasyan"
        }

        director = self.director_service.update(data)

        assert isinstance(director, Director)
        assert director.id is not None
        assert director.name is not None

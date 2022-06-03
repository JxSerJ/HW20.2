from unittest.mock import MagicMock

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService

import pytest


@pytest.fixture
def movie_dao():
    movie_dao = MovieDAO(None)

    m1 = Movie(id=1, title="mov1_title", description="mov1_desc", trailer="mov1_trailer", year=1990, rating=1,
               genre_id=1, director_id=1)
    m2 = Movie(id=2, title="mov2_title", description="mov2_desc", trailer="mov2_trailer", year=1991, rating=2,
               genre_id=2, director_id=2)
    m3 = Movie(id=3, title="mov3_title", description="mov3_desc", trailer="mov3_trailer", year=1992, rating=3,
               genre_id=3, director_id=3)

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=[m1, m2, m3])
    movie_dao.create = MagicMock(return_value=Movie(id=4))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock(return_value=Movie(id=1))

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(2)

        assert movie is not None
        assert isinstance(movie, Movie)
        assert movie.id is not None
        assert movie.title == 'mov1_title'

    def test_get_all(self):
        movies = self.movie_service.get_all()

        assert len(movies) > 0
        assert isinstance(movies[0], Movie)
        assert movies[0].title == 'mov1_title'

    def test_create(self):
        data = {
            "title": "Чикаго",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "year": 2002,
            "rating": 7.2,
            "genre_id": 18,
            "director_id": 6
        }

        new_movie = self.movie_service.create(data)

        assert new_movie is not None
        assert new_movie.id == 4
        assert isinstance(new_movie, Movie)

    def test_update(self):
        data = {
            "title": "Чикаго",
            "description": "Рокси Харт мечтает о песнях и танцах и о том, как сравняться с самой Велмой Келли, примадонной водевиля. И Рокси действительно оказывается с Велмой в одном положении, когда несколько очень неправильных шагов приводят обеих на скамью подсудимых.",
            "trailer": "https://www.youtube.com/watch?v=YxzS_LzWdG8",
            "year": 2002,
            "rating": 7.2,
            "genre_id": 18,
            "director_id": 6,
            "id": 1
        }

        upd_movie = self.movie_service.update(data)

        assert upd_movie is not None
        assert isinstance(upd_movie, Movie)
        assert upd_movie.id == 1

    def test_delete(self):
        result = self.movie_service.delete(1)

        assert result is None
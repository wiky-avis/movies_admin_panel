from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

BLOCK_SIZE = 100
TABLES = ("film_work", "genre", "genre_film_work", "person", "person_film_work")
MODELS = (FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork)

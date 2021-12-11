from dataclasses import dataclass
from datetime import date


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    creation_date: str
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: str
    updated_at: str


@dataclass
class Genre:
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created_at: str


@dataclass
class Person:
    id: str
    full_name: str
    birth_date: date
    created_at: str
    updated_at: str


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: str

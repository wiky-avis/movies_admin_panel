import uuid
from dataclasses import dataclass
from datetime import datetime, timezone, date


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    creation_date: str or None
    certificate: str or None
    file_path: str or None
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

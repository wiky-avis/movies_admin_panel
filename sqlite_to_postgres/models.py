from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class FilmWork:
    id: str
    title: str
    description: Optional[str]
    creation_date: Optional[str]
    certificate: Optional[str]
    file_path: Optional[str]
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Genre:
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


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
    birth_date: Optional[date]
    created_at: datetime
    updated_at: datetime


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime

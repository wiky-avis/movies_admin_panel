import uuid
from dataclasses import dataclass
from datetime import datetime, timezone, date


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    creation_date: datetime.utcnow().replace(tzinfo=timezone.utc)
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime.utcnow().replace(tzinfo=timezone.utc)
    updated_at: datetime.utcnow().replace(tzinfo=timezone.utc)


@dataclass
class Genre:
    id: str
    name: str
    description: str
    created_at: datetime.utcnow().replace(tzinfo=timezone.utc)
    updated_at: datetime.utcnow().replace(tzinfo=timezone.utc)


@dataclass
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created_at: datetime.utcnow().replace(tzinfo=timezone.utc)


@dataclass
class Person:
    id: str
    full_name: str
    birth_date: date
    created_at: datetime.utcnow().replace(tzinfo=timezone.utc)
    updated_at: datetime.utcnow().replace(tzinfo=timezone.utc)


@dataclass
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: datetime.utcnow().replace(tzinfo=timezone.utc)

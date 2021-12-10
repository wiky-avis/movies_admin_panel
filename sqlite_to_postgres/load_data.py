from dataclasses import dataclass
import sqlite3
from pprint import pprint
from datetime import datetime
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

tables_names = ["film_work", "genre", "genre_film_work", "person", "person_film_work"]


class SQLiteLoader:

    __select_query_film_work = """SELECT * FROM film_work ORDER BY id"""
    __select_query_genre = """SELECT * FROM genre ORDER BY id"""
    __select_query_genre_film_work = """SELECT * FROM genre_film_work ORDER BY id"""
    __select_query_person = """SELECT * FROM person ORDER BY id"""
    __select_query_person_film_work = """SELECT * FROM person_film_work ORDER BY id"""

    def __init__(self, conn):
        self.conn = conn

    def get_film_work(self):
        cursor = self.conn.cursor()
        films = tuple(cursor.execute(self.__select_query_film_work))
        for data in films:
            yield FilmWork(*data)

    def get_genre(self):
        cursor = self.conn.cursor()
        genres = tuple(cursor.execute(self.__select_query_genre))
        for data in genres:
            yield Genre(*data)

    def get_genre_film_work(self):
        cursor = self.conn.cursor()
        genre_film_work = tuple(cursor.execute(self.__select_query_genre_film_work))
        for data in genre_film_work:
            yield GenreFilmWork(*data)

    def get_persons(self):
        cursor = self.conn.cursor()
        persons = tuple(cursor.execute(self.__select_query_person))
        for data in persons:
            yield Person(*data)

    def get_person_film_work(self):
        cursor = self.conn.cursor()
        person_film_work = tuple(cursor.execute(self.__select_query_person_film_work))
        for data in person_film_work:
            yield PersonFilmWork(*data)


class PostgresSaver:

    def save_all_data(self, data):
        pass


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    film_work = sqlite_loader.get_film_work()
    genres = sqlite_loader.get_genre()
    genre_film_work = sqlite_loader.get_genre_film_work()
    persons = sqlite_loader.get_persons()
    person_film_work = sqlite_loader.get_person_film_work()

    pg_cursor = pg_conn.cursor()

    pg_cursor.executemany(
        """INSERT INTO content.film_work (
        id, title, description, creation_date, certificate, file_path, rating, type, created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);""",
        [
            (
                film.id,
                film.title,
                film.description,
                film.creation_date,
                film.certificate,
                film.file_path,
                film.rating,
                film.type,
                film.created_at,
                film.updated_at
            ) for film in film_work
        ]
    )



    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'moviesdb', 'user': 'userdb', 'password': 'password', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

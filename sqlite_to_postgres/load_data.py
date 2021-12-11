from dataclasses import astuple
import sqlite3
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_values


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
        films = cursor.execute(self.__select_query_film_work)
        list_data = [astuple(FilmWork(*data)) for data in films]
        return list_data

    def get_genre(self):
        cursor = self.conn.cursor()
        genres = cursor.execute(self.__select_query_genre)
        list_data = [astuple(Genre(*data)) for data in genres]
        return list_data

    def get_genre_film_work(self):
        cursor = self.conn.cursor()
        genre_film_work = cursor.execute(self.__select_query_genre_film_work)
        list_data = [astuple(GenreFilmWork(*data)) for data in genre_film_work]
        return list_data

    def get_persons(self):
        cursor = self.conn.cursor()
        persons = cursor.execute(self.__select_query_person)
        list_data = [astuple(Person(*data)) for data in persons]
        return list_data

    def get_person_film_work(self):
        cursor = self.conn.cursor()
        person_film_work = cursor.execute(self.__select_query_person_film_work)
        list_data = [astuple(PersonFilmWork(*data)) for data in person_film_work]
        return list_data

    def __call__(self):
        return {
            "film_work": self.get_film_work(),
            "genre": self.get_genre(),
            "genre_film_work": self.get_genre_film_work(),
            "person": self.get_persons(),
            "person_film_work": self.get_person_film_work()
        }


class PostgresSaver:

    def __init__(self, conn):
        self.pg_conn = conn
        self.cursor = self.pg_conn.cursor()

    def save_all_data(self, data: list, table_name: str):
        execute_values(
            self.cursor,
            """INSERT INTO content.{} VALUES %s;""".format(table_name), data, page_size=100
        )

        self.pg_conn.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    get_data = sqlite_loader()

    for table_name, data in get_data.items():
        postgres_saver.save_all_data(data, table_name)


if __name__ == '__main__':
    dsl = {'dbname': 'moviesdb', 'user': 'userdb', 'password': 'password', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

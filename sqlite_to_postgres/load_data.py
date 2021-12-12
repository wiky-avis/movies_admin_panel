import sqlite3
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from actions import SQLiteLoader, PostgresSaver

TABLES = ("film_work", "genre", "genre_film_work", "person", "person_film_work")
MODELS = (FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    for table_name, model in zip(TABLES, MODELS):
        sqlite_loader = SQLiteLoader(connection, table_name, model)
        get_data = sqlite_loader()
        postgres_saver = PostgresSaver(pg_conn)
        postgres_saver(get_data, table_name)


if __name__ == '__main__':
    dsl = {'dbname': 'moviesdb', 'user': 'userdb', 'password': 'password', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

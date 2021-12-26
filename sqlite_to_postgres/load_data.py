import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from actions import SQLiteLoader, PostgresSaver
from consts import TABLES, MODELS


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    for table_name, model in zip(TABLES, MODELS):
        sqlite_loader = SQLiteLoader(connection)
        get_data = sqlite_loader(table_name, model)
        postgres_saver = PostgresSaver(pg_conn)
        postgres_saver(get_data, table_name)


if __name__ == '__main__':
    dsl = {'dbname': 'moviesdb', 'user': 'userdb', 'password': 'password', 'host': 'db', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

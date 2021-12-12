import psycopg2
from psycopg2.extras import DictCursor


class PostgresCreateSchemaDb:

    def __init__(self, connection):
        self.cursor = connection.cursor()

    def create_shema_db(self):
        self.cursor.execute("""CREATE SCHEMA IF NOT EXISTS content;""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS content.genre (
                    id uuid PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at timestamp with time zone,
                    updated_at timestamp with time zone
                );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS content.film_work (
                     id uuid PRIMARY KEY,
                     title TEXT NOT NULL,
                     description TEXT,
                     creation_date DATE,
                     certificate TEXT,
                     file_path TEXT,
                     rating FLOAT,
                     type TEXT NOT NULL,
                     created_at timestamp with time zone,
                     updated_at timestamp with time zone
                );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS content.person (
                     id uuid PRIMARY KEY,
                     full_name TEXT NOT NULL,
                     birth_date DATE,
                     created_at timestamp with time zone,
                     updated_at timestamp with time zone
                );""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS content.genre_film_work (
                     id uuid PRIMARY KEY,
                     film_work_id uuid NOT NULL,
                     genre_id uuid NOT NULL,
                     created_at timestamp with time zone
                    );""")

        self.cursor.execute("""CREATE UNIQUE INDEX film_work_genre ON content.genre_film_work (film_work_id, genre_id);""")

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS content.person_film_work (
                     id uuid PRIMARY KEY,
                     film_work_id uuid NOT NULL,
                     person_id uuid NOT NULL,
                     role TEXT NOT NULL,
                     created_at timestamp with time zone
                );""")

        self.cursor.execute(
            """CREATE UNIQUE INDEX film_work_person_role ON content.person_film_work (film_work_id, person_id, role);""")

    def __call__(self):
        self.create_shema_db()


if __name__ == '__main__':
    dsl = {'dbname': 'moviesdb', 'user': 'userdb', 'password': 'password', 'host': '127.0.0.1', 'port': 5432}
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        postgres_creator = PostgresCreateSchemaDb(pg_conn)
        postgres_creator()

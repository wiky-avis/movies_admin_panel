import uuid
import sqlite3
from datetime import datetime, timezone


class GetDataFromDB:
    SQL = """
        WITH x as (
        SELECT 
        m.id, 
        group_concat(a.id) as actors_ids, 
        group_concat(a.name) as actors_names, 
        group_concat(w.name) as writer_name 
        FROM movies m
        LEFT JOIN movie_actors ma on m.id = ma.movie_id
        LEFT JOIN actors a on ma.actor_id = a.id
        LEFT JOIN writers w on m.writer = w.id
        GROUP BY m.id
        )
        SELECT m.id, genre, director, writer, writer_name, title, plot, imdb_rating, x.actors_names,
        CASE
        WHEN m.writers = '' THEN '[{"id": "' || m.writer || '"}]' ELSE m.writers END AS w 
        FROM movies m LEFT JOIN x ON m.id = x.id
    """

    def __init__(self, cursor, cursor_new):
        self.cursor = cursor
        self.cursor_new = cursor_new

    def get_data_movies(self):
        return tuple(self.cursor.execute(self.SQL))

    def get_films(self):
        data_sql_films = self.cursor_new.execute(
            """SELECT id, title FROM film_work;"""
        )
        films = [(film[0], film[1]) for film in data_sql_films]
        return films

    def get_persons(self):
        return tuple(self.cursor_new.execute(f"""SELECT id, full_name FROM person;"""))

    def get_genres(self):
        movies = self.get_data_movies()
        genres = []
        genres_2 = []

        for genre in movies:
            movie = genre[5]
            genre = genre[1].split(", ")
            for i in genre:
                genres.append((i, movie))
        data_sql_genre = self.cursor_new.execute("""SELECT id, name FROM genre""")

        for genre_2 in data_sql_genre:
            for genre in genres:
                if genre_2[1] == genre[0]:
                    genres_2.append((str(uuid.uuid4()), genre_2[0], genre_2[1], genre[1]))
        return genres_2

    def get_actors(self):
        movies = self.get_data_movies()
        actors = []

        for actor in movies:
            if actor[8]:
                actor_names = actor[8].split(",")
                for i in actor_names:
                    if i is not None and i != 'N/A' and i != '':
                        actors.append((i, actor[5], "actor"))
        return actors

    def get_directors(self):
        movies = self.get_data_movies()
        directors = []
        for director in movies:
            for i in director[2].split(", "):
                if i != 'N/A':
                    directors.append((i, director[5], "director"))
        return directors

    def get_writers(self):
        movies = self.get_data_movies()
        writers = []

        for writer in movies:
            if writer[4]:
                writer_names = writer[4].split(",")
                if writer_names[0] is not None and writer_names[0] != 'N/A' and writer_names[0] != '':
                    writers.append((writer_names[0], writer[5], "writer"))
        return writers


class LoadDataFromNewDb(GetDataFromDB):
    def create_tables(self):
        self.cursor_new.execute("""
         CREATE TABLE IF NOT EXISTS genre (
         id uuid PRIMARY KEY, 
         name TEXT NOT NULL, 
         description TEXT, 
         created_at timestamp with time zone, 
         updated_at timestamp with time zone
        );
        """)

        self.cursor_new.execute("""CREATE TABLE IF NOT EXISTS film_work (
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

        self.cursor_new.execute("""CREATE TABLE IF NOT EXISTS person (
         id uuid PRIMARY KEY,
         full_name TEXT NOT NULL,
         birth_date DATE,
         created_at timestamp with time zone,
         updated_at timestamp with time zone
        );""")

        self.cursor_new.execute("""CREATE TABLE IF NOT EXISTS genre_film_work (
         id uuid PRIMARY KEY,
         film_work_id uuid NOT NULL,
         genre_id uuid NOT NULL,
         created_at timestamp with time zone
        );""")

        self.cursor_new.execute("""CREATE TABLE IF NOT EXISTS person_film_work (
         id uuid PRIMARY KEY,
         film_work_id uuid NOT NULL,
         person_id uuid NOT NULL,
         role TEXT NOT NULL,
         created_at timestamp with time zone
        );""")

    def load_genres(self):
        movies = self.get_data_movies()
        genres = set()
        for genre in movies:
            genre = genre[1].split(", ")
            for i in genre:
                genres.add(i)
        self.cursor_new.executemany(
            """INSERT INTO genre(id, name, created_at, updated_at) VALUES($1, $2, $3, $4)""",
            [
                (
                    str(uuid.uuid4()),
                    genre,
                    datetime.utcnow().replace(tzinfo=timezone.utc),
                    datetime.utcnow().replace(tzinfo=timezone.utc)
                ) for genre in genres
            ]
        )

    def load_person(self):
        movies = self.get_data_movies()
        writers = [person[0] for person in
                   self.cursor.execute("""SELECT DISTINCT name FROM writers WHERE name!='N/A'""")]
        actors = [
            person[0] for person in self.cursor.execute("""SELECT DISTINCT name FROM actors WHERE name!='N/A'""")
        ]
        directors = [person[2] for person in movies if person[2] != 'N/A']
        persons = set(writers + actors + directors)

        self.cursor_new.executemany(
            """INSERT INTO person(id, full_name, created_at, updated_at) VALUES($1, $2, $3, $4)""",
            [
                (
                    str(uuid.uuid4()),
                    person,
                    datetime.utcnow().replace(tzinfo=timezone.utc),
                    datetime.utcnow().replace(tzinfo=timezone.utc)
                ) for person in set(persons)
            ]
        )

    def load_film_work(self):
        movies = self.get_data_movies()

        self.cursor_new.executemany(
            """
            INSERT INTO film_work(id, title, description, type, rating, created_at, updated_at) 
            VALUES($1, $2, $3, $4, $5, $6, $7)
            """,
            [
                (
                    str(uuid.uuid4()),
                    film[5],
                    film[6],
                    "movies",
                    film[7],
                    datetime.utcnow().replace(tzinfo=timezone.utc),
                    datetime.utcnow().replace(tzinfo=timezone.utc)
                ) for film in movies
            ]
        )

    def load_genre_film_work(self):
        films = self.get_films()
        genres = self.get_genres()

        genre_film_work = []
        unique_genre_ids = set()
        for genre in genres:
            for film in films:
                if genre[3] == film[1] and genre[0] not in unique_genre_ids:
                    genre_film_work.append((genre[0], film[0], genre[1]))
                    unique_genre_ids.add(genre[0])

        self.cursor_new.executemany(
            """INSERT INTO genre_film_work(id, film_work_id, genre_id, created_at) VALUES($1, $2, $3, $4);""",
            [
                (
                    str(uuid.uuid4()),
                    genre[1],
                    genre[2],
                    datetime.utcnow().replace(tzinfo=timezone.utc),
                ) for genre in genre_film_work
            ]
        )

    def load_person_film_work(self):
        actors = self.get_actors()
        directors = self.get_directors()
        writers = self.get_writers()

        persons_ls = directors + writers + actors
        persons = self.get_persons()

        data_persons = []
        for person in persons_ls:
            for person_2 in persons:
                if person[0] == person_2[1]:
                    data_persons.append((person_2[0], person[0], person[1], person[2]))

        films = self.get_films()

        data_persons_finally = []
        for person in data_persons:
            for film in films:
                if person[2] == film[1]:
                    data_persons_finally.append((person[0], person[1], film[0], person[3]))

        self.cursor_new.executemany(
            """
            INSERT INTO person_film_work(id, film_work_id, person_id, role, created_at) VALUES($1, $2, $3, $4, $5);
            """,
            [
                (
                    str(uuid.uuid4()),
                    person[2],
                    person[0],
                    person[3],
                    datetime.utcnow().replace(tzinfo=timezone.utc),
                ) for person in data_persons_finally
            ]
        )

    def __call__(self):
        self.create_tables()
        self.load_genres()
        self.load_person()
        self.load_film_work()
        self.load_genre_film_work()
        self.load_person_film_work()


if __name__ == "__main__":
    with sqlite3.connect('db.sqlite') as sqlite_conn, sqlite3.connect('new_db.sqlite') as new_sqlite_conn:
        cursor = sqlite_conn.cursor()
        cursor_new = new_sqlite_conn.cursor()
        load_to_new_db = LoadDataFromNewDb(cursor, cursor_new)
        load_to_new_db()

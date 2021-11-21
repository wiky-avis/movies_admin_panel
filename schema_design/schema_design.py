import uuid
import sqlite3
from datetime import datetime, timezone


def load_genres(cursor):
    data_sql = cursor.execute("""SELECT DISTINCT genre FROM movies""")
    genres = set()
    for genre in data_sql:
        genre = genre[0].split(", ")
        for i in genre:
            genres.add(i)
    cursor.executemany(
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


def load_person(cursor):
    writers = [person[0] for person in cursor.execute("""SELECT DISTINCT name FROM writers WHERE name!='N/A'""")]
    actors = [person[0] for person in cursor.execute("""SELECT DISTINCT name FROM actors WHERE name!='N/A'""")]
    directors = [
        person[0] for person in cursor.execute("""SELECT DISTINCT director FROM movies WHERE director!='N/A'""")
    ]
    persons = writers + actors + directors
    cursor.executemany(
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


if __name__ == "__main__":
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    load_genres(cursor)
    load_person(cursor)

    conn.commit()
    conn.close()

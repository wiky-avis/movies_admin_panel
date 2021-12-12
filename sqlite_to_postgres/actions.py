from dataclasses import astuple
from psycopg2.extras import execute_values
from typing import List

from sqlite_to_postgres.consts import BLOCK_SIZE


class SQLiteLoader:

    __select_query = """SELECT * FROM {0} ORDER BY id"""

    def __init__(self, conn):
        self.cursor = conn.cursor()

    def __call__(self, table_name, model) -> List[List[tuple]]:
        self.cursor.execute(self.__select_query.format(table_name))
        while True:
            page = self.cursor.fetchmany(BLOCK_SIZE)
            if not page:
                break
            parts = []
            for data in page:
                parts.append(astuple(model(*data)))
            yield parts


class PostgresSaver:

    def __init__(self, conn):
        self.pg_conn = conn
        self.cursor = self.pg_conn.cursor()

    def __call__(self, pages, table_name):
        for page in pages:
            execute_values(
                self.cursor,
                """INSERT INTO content.{0} VALUES %s;""".format(table_name), page, page_size=BLOCK_SIZE
            )

        self.pg_conn.commit()

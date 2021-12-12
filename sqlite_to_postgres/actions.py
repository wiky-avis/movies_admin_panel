from dataclasses import astuple
from psycopg2.extras import execute_values


class SQLiteLoader:

    __select_query = """SELECT * FROM {0} ORDER BY id"""

    def __init__(self, conn, table_name, model):
        self.cursor = conn.cursor()
        self.table_name = table_name
        self.model = model

    def __call__(self):
        self.cursor.execute(self.__select_query.format(self.table_name))
        while True:
            page = self.cursor.fetchmany(100)
            if not page:
                break
            parts = []
            for data in page:
                parts.append(astuple(self.model(*data)))
            yield parts


class PostgresSaver:

    def __init__(self, conn):
        self.pg_conn = conn
        self.cursor = self.pg_conn.cursor()

    def __call__(self, pages, table_name):
        for page in pages:
            execute_values(
                self.cursor,
                """INSERT INTO content.{0} VALUES %s;""".format(table_name), page, page_size=100
            )

        self.pg_conn.commit()

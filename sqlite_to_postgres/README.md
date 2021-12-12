
# sqlite_to_postgres
Перенос данных из SQLite в Postgres


Запустить контейнер с Postgresql и спроектировать БД для переноса [контейнер и инструкция тут](https://github.com/wiky-avis/psql-container.git).

Создайте базу данных и таблицы в Postgresql по примеру из файла [schema_design](schema_design.txt) или запустите скрипт `python schema_design.py`.

Запустите скрипт:

    `python load_data.py`


После запуска скрипт автоматически загрузит данные в базу Postgresql. В комплекте тестовая база SQLite.

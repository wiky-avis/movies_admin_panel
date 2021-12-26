#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Создание схемы БД"
cd sqlite_to_postgres
python schema_design.py
echo "Загрузка данных из sqlite"
python load_data.py
echo "Загрузка завершена"

cd ..
cd movies_admin

python manage.py migrate movies --fake
python manage.py migrate

python manage.py collectstatic --no-input

exec gunicorn config.wsgi:application --bind 0.0.0.0:8000

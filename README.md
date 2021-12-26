# Admin panel

Описание структуры проекта:
1. `schema_design` - раздел c материалами для новой архитектуры базы данных.
2. `sqlite_to_postgres` - раздел с материалами по миграции данных.
3. `movies_admin` - раздел с материалами для панели администратора.


Запуск приложения:

    `docker-compose up -d`

Зайти в контейнер и создать пользователя для доступа в админ панель:

    `docker exec -it movies_admin_panel_web_1 bash`


    `cd movies_admin && python manage.py createsuperuser`

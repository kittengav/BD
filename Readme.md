# Описание

Программа представляет собой веб-приложение. Пользовательский интерфейс реализован в браузере.\
При запросах к базе данных не используются готовые ORM. Вместо этого реализован
собственный генератор запросов.

# Запуск
## Если у вас на компьютере установлен Docker:
````shell
docker-compose build
docker-compose up
````
Приложение доступно по http://localhost:8000/ \
База данных доступна на порту 5431

## Если у вас на компьютере нет Docker:\
\
Установить PostgreSQL версии 11+\
Установать python версии 3.11+\
Создать базу данных \
Передать ей запрос из ./sql_requests/create_tables_script.sql\
Указать ее настройки в .env\
Возможно прийдется настроить config.py\
````shell
pip install req.txt
uvicorn main:app
````
Приложение доступно по http://localhost:8000/ \




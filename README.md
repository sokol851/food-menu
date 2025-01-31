# Сервис для работы с меню ресторана

### API создан на DRF для вывода списка категорий и списком их опубликованных блюд, хранимых в PostgreSQL, если эти категории не пустые.

## Запуск

#### Docker-Compose

```
    1) Изменить .env.simple на .env
    2) Внести в него изменения
    3) Выполнить команду "docker-compose up -d --build"
```

#### Локально

```
    1) Изменить .env.simple на .env
    2) Внести в него изменения
    3) Применить миграции "python manage.py makemigrations && python manage.py migrate"
    4) Запустить сервер "python manage.py runserver"
```

## Тесты

```
    1) Выполнить команду "coverage run --source='.' manage.py test"
    2) Вывести тесты "coverage report" или "coverage html"
```

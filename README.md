# django-base-docker

Базовый шаблон проекта Django для обучения коллег работе с Django внутри Docker-контейнеров.

## Описание

- Проект предназначен для знакомства с современным подходом к разработке Django-приложений в изолированной среде Docker.
- В шаблоне отсутствуют пользовательские Django-приложения, чтобы не усложнять код и сосредоточиться на инфраструктуре.
- Используется асинхронный сервер приложений (ASGI, Uvicorn).
- В будущем планируется добавить интеграцию с Celery, RabbitMQ, Redis и другими сервисами.
- Проект легко расширяется под любые задачи.

## Состав
- Django (ASGI-ready)
- Postgres (через Docker)
- Nginx (для production)
- Готовые конфиги для dev/prod окружения
- Пример .env файла

## Как развернуть проект

1. **Клонируйте репозиторий:**
   ```bash
   git clone <адрес-репозитория>
   cd django-base-docker
   ```

2. **Создайте файл .env:**
   ```bash
   cp .env.example .env
   # или создайте вручную, см. пример ниже
   ```

3. **Запустите проект в режиме разработки:**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
   ```
   - Приложение будет доступно на http://localhost:8000
   - Админка Django: http://localhost:8000/admin/
   - PgAdmin (для работы с БД): http://localhost:5050
   - Для отладки используется Debugpy и порт прослушивания 5678, подключаться к локальному хосту где запущены контейнеры

4. **Остановить проект:**
   ```bash
   docker compose down
   ```

5. **Выполнить миграции или другие команды Django внутри контейнера:**
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

6. **Собрать статику (production):**
   ```bash
   docker compose exec web python manage.py collectstatic --noinput
   ```

## Пример .env файла

```env
# Postgres
POSTGRES_DB=django_db
POSTGRES_USER=root
POSTGRES_PASSWORD=test
POSTGRES_HOST=db
POSTGRES_PORT=5432

# PG Admin
PGADMIN_DEFAULT_EMAIL=admin@test.ru
PGADMIN_DEFAULT_PASSWORD=test

# Django
DJANGO_SECRET_KEY=django-insecure-tp2xfipkc527p3v7j-@$y9$03k!x&l14r2+g@ai9q)cu8q4j2b
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DJANGO_TIME_ZONE=Europe/Moscow
DJANGO_LANGUAGE_CODE=ru-RU
```

## Полезные команды

- Запуск в режиме разработки:
  ```bash
  docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
  ```
- Запуск в production:
  ```bash
  docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
  ```
- Остановка:
  ```bash
  docker compose down
  ```
- Миграции:
  ```bash
  docker compose exec web python manage.py migrate
  ```
- Создание суперпользователя:
  ```bash
  docker compose exec web python manage.py createsuperuser
  ```
- Сборка статики:
  ```bash
  docker compose exec web python manage.py collectstatic --noinput
  ```
- Просмотр логов:
  ```bash
  docker compose logs -f web
  ```

---

**В будущем планируется добавить интеграцию с Celery, RabbitMQ, Redis и другими сервисами для асинхронных задач и очередей.**

---

Если возникнут вопросы — смело обращайтесь!

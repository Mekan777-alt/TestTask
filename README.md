# Metrics API

REST API для управления метриками с JWT авторизацией, кэшированием и админ-панелью.

## Стек технологий

- Python 3.11, FastAPI, SQLAlchemy 2.0 (asyncpg)
- PostgreSQL 16, Redis 7
- Celery (Beat), starlette-admin
- Docker, docker-compose

## Структура проекта

```
src/
├── api/                  # Контроллеры, сервисы, репозитории, DTO
├── admin/                # Админ-панель (views, auth)
├── core/                 # Конфигурация, безопасность, Celery-задачи
├── database/             # Сессия, базовый репозиторий, Redis
├── models/               # ORM-модели
├── migrations/           # Alembic миграции
├── tests/                # Тесты (pytest + httpx)
├── api_app.py            # FastAPI приложение
├── admin_app.py          # Starlette-admin приложение
└── celery_app.py         # Celery конфигурация
```

## Запуск через Docker

1. Создать `.env` из шаблона и при необходимости отредактировать:

```bash
cp .env.example .env
```

Для Docker изменить хосты в `.env`:

```env
DB_HOST=database
REDIS_HOST=redis
```

2. Запустить:

```bash
docker-compose up --build
```

Будет поднято 4 сервиса:
- **api** — FastAPI на порту 8000
- **database** — PostgreSQL
- **redis** — Redis
- **celery** — Celery worker + Beat

## Локальный запуск (без Docker)

### Linux / macOS

1. Создать виртуальное окружение и установить зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Создать `.env` из шаблона и при необходимости отредактировать:

```bash
cp .env.example .env
```

3. Запустить PostgreSQL и Redis.

4. Применить миграции:

```bash
alembic upgrade head
```

5. Запустить API:

```bash
cd src && uvicorn api_app:app --reload
```

6. Запустить Celery worker + Beat:

```bash
cd src && celery -A celery_app worker -B --loglevel INFO
```

### Windows

1. Создать виртуальное окружение и установить зависимости:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Создать `.env` из шаблона и при необходимости отредактировать:

```cmd
copy .env.example .env
```

3. Запустить PostgreSQL и Redis.

4. Применить миграции:

```cmd
alembic upgrade head
```

5. Запустить API:

```cmd
cd src && uvicorn api_app:app --reload
```

6. Запустить Celery worker + Beat:

```cmd
cd src && celery -A celery_app worker -B --loglevel INFO
```

## Доступ

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
- Админ-панель: http://127.0.0.1:8000/admin
- Логин админки по умолчанию: `admin` / `admin123`

## API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/v1/auth/token` | Получение JWT токена |
| POST | `/api/v1/auth/refresh` | Обновление токенов |
| POST | `/api/v1/auth/logout` | Выход из системы |
| GET | `/api/v1/auth/me` | Данные о себе |
| POST | `/api/v1/metrics` | Создание метрики |
| GET | `/api/v1/metrics` | Список метрик пользователя |
| GET | `/api/v1/metrics/{id}/records` | Список записей метрики (кэшируется) |
| POST | `/api/v1/metrics/{id}/records` | Создание записи метрики |
| GET | `/api/v1/metrics/{id}/records/{id}` | Детализация записи |
| GET | `/api/v1/tags` | Список тегов |

## Тесты

```bash
cd src && python -m pytest tests/ -v
```

## Линтеры

```bash
ruff check src/
mypy src/
```

## Celery Beat

Каждые 2 минуты создает/обновляет файл `reports/report.txt` с количеством метрик и записей в базе.

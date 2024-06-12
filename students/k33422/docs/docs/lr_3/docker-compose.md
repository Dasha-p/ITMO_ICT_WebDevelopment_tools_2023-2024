# Документация Docker Compose

Этот файл `docker-compose.yml` используется для определения и конфигурации сервисов, необходимых для запуска приложения в
контейнерах Docker.

## Сервис `postgres`

```yaml
postgres:
  container_name: postgres
  image: postgres:16-alpine
  restart: always
  environment:
    - POSTGRES_USER=${DB_USER}
    - POSTGRES_PASSWORD=${DB_PASSWORD}
    - POSTGRES_DB=${DB_NAME}
  env_file:
    - .env
  ports:
    - "5432:5432"
  healthcheck:
    test: [ "CMD-SHELL", "pg_isready -U ${DB_USER}" ]
    interval: 10s
    timeout: 5s
    retries: 5
  volumes:
    - pgdata:/var/lib/postgresql/data
```

Этот сервис определяет контейнер PostgreSQL. Он использует образ `postgres:16-alpine` и настраивает следующие параметры:

- `container_name`: Устанавливает имя контейнера в `postgres`.
- `restart`: Политика перезапуска установлена в `always`, чтобы контейнер автоматически перезапускался в случае сбоя.
- `environment`: Определяет переменные окружения для конфигурации PostgreSQL, такие как имя пользователя, пароль и имя базы
  данных. Значения берутся из файла `.env`.
- `env_file`: Указывает файл `.env` для загрузки переменных окружения.
- `ports`: Проксирует порт 5432 контейнера на порт 5432 хоста.
- `healthcheck`: Настраивает проверку работоспособности контейнера с помощью команды `pg_isready`.
- `volumes`: Монтирует том `pgdata` для сохранения данных PostgreSQL.

## Сервис `redis`

```yaml
redis:
  image: redis:7-alpine
  restart: always
  ports:
    - "6379:6379"
  healthcheck:
    test: [ "CMD", "redis-cli", "ping" ]
    interval: 10s
    timeout: 5s
    retries: 5
```

Этот сервис определяет контейнер Redis. Он использует образ `redis:7-alpine` и настраивает следующие параметры:

- `restart`: Политика перезапуска установлена в `always`, чтобы контейнер автоматически перезапускался в случае сбоя.
- `ports`: Проксирует порт 6379 контейнера на порт 6379 хоста.
- `healthcheck`: Настраивает проверку работоспособности контейнера с помощью команды `redis-cli ping`.

## Сервис `celery`

```yaml
celery:
  container_name: celery
  build: .
  command: python -m celery -A src.services.celery_worker worker -l info
  depends_on:
    redis:
      condition: service_healthy
    postgres:
      condition: service_healthy
```

Этот сервис определяет контейнер Celery. Он использует Dockerfile в текущей директории для сборки образа и настраивает
следующие параметры:

- `container_name`: Устанавливает имя контейнера в `celery`.
- `command`: Указывает команду для запуска рабочего процесса Celery.
- `depends_on`: Определяет зависимости сервиса от контейнеров `redis` и `postgres`. Сервис будет запущен только после того, как
  эти контейнеры будут здоровы.

## Сервис `fastapi`

```yaml
fastapi:
  container_name: fastapi
  build: .
  command: python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
  ports:
    - "8000:8000"
  depends_on:
    redis:
      condition: service_healthy
    postgres:
      condition: service_healthy
    celery:
      condition: service_started
```

Этот сервис определяет контейнер FastAPI. Он использует Dockerfile в текущей директории для сборки образа и настраивает
следующие параметры:

- `container_name`: Устанавливает имя контейнера в `fastapi`.
- `command`: Указывает команду для запуска приложения FastAPI с помощью Uvicorn.
- `ports`: Проксирует порт 8000 контейнера на порт 8000 хоста.
- `depends_on`: Определяет зависимости сервиса от контейнеров `redis`, `postgres` и `celery`. Сервис будет запущен только после
  того, как `redis` и `postgres` будут здоровы, а `celery` будет запущен.

## Тома

```yaml
volumes:
  pgdata:
```

В разделе `volumes` определяется именованный том `pgdata`, который используется для сохранения данных PostgreSQL.

---

Для запуска приложения с использованием этой конфигурации Docker Compose, вы можете выполнить следующую команду в директории,
содержащей файл `docker-compose.yml`:

```bash
docker-compose up -d
```

Эта команда запустит все сервисы, определенные в файле `docker-compose.yml`, в фоновом режиме (`-d`).

Чтобы остановить и удалить контейнеры, вы можете использовать команду:

```bash
docker-compose down
```

Эта конфигурация Docker Compose обеспечивает скоординированный запуск сервисов приложения, включая базу данных PostgreSQL,
Redis, Celery и FastAPI. Она также настраивает проверки работоспособности и зависимости между сервисами для обеспечения
правильного порядка запуска и работы приложения.
# Подключение базы данных

## Описание

Для подключения базы данных к проекту был использован асинхронный драйвер `asyncpg`.
DNS формировался динамически в зависимости от заданных параметров в переменных локального окружения.
Для удобства вызова сессий был реализован класс `Helper`, который предоставляет базовый интерфейс.
Методы класса реализую асинхронное подключение к базе данных для повышения производительности всего приложения.

`config.py`

```python
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    scheme: str
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(
        env_prefix='db_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def url(self) -> PostgresDsn:
        return f"{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


settings = Settings()
```

`helper.py`

```python
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession
)

from src.db.config import settings


class Helper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


helper = Helper(
    url=settings.url,
)
```
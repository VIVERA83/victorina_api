"""Database..."""
from typing import Optional, Type

from base.base_accessor import BaseAccessor
from core.settings import Settings
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    """Настройка мета данных.

    В частности указываем схему для хранения таблиц."""

    metadata = MetaData(schema=Settings().postgres.db_schema)
    id: Optional[Mapped] = None

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

    __str__ = __repr__


class Database(BaseAccessor):
    """Описание правил потключения PostgresQL к приложению Fast-Api"""

    _engine: Optional[AsyncEngine] = None
    _db: Optional[Type[DeclarativeBase]] = None
    session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict):
        """Подключение к базе данных."""
        self._db = Base
        self._engine = create_async_engine(
            self.app.settings.postgres.dsn, echo=False, future=True
        )
        self.session = AsyncSession(self._engine, expire_on_commit=False)
        self.logger.info("Connected to Postgres")

    async def disconnect(self, *_: list, **__: dict):
        """Закрытие потключения."""
        if self._engine:
            await self._engine.dispose()
        self.logger.info("Disconnected from Postgres")

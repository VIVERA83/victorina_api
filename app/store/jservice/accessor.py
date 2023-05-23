"""JServiceAccessor."""
from typing import TYPE_CHECKING, Optional

from aiohttp import TCPConnector
from aiohttp.client import ClientSession
from base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from core.app import Application

API_PATH = "https://jservice.io/api/"


class JServiceAccessor(BaseAccessor):
    """Описание правил потключения JService к приложению Fast-Api.
    "https://jservice.io/api/"""

    session: Optional[ClientSession]

    def _init_(self, app: "Application", *_: list, **__: dict):
        """Дополнительные настройки."""
        self.session = None

    async def connect(self, *_: "Application"):
        """Создание клиентской сессии."""
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.logger.info("JService is ready")

    async def disconnect(self, *_: "Application"):
        """Закрытие клиентской сессии."""
        await self.session.close()
        self.logger.info("JService is closed")

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        """Создаем URL для обращения к сервису."""
        url = host + method + "?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def get_random_questions(self, count: int) -> list:
        """Запрос на получения случайных впрососов."""
        method = "random/"
        url = self._build_query(API_PATH, method, {"count": count})
        async with self.session.get(url) as resp:
            return await resp.json()

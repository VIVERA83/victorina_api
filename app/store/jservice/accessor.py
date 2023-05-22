from typing import Optional, TYPE_CHECKING

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from core.app import Application

API_PATH = "https://jservice.io/api/"


# random?count=20

class JServiceAccessor(BaseAccessor):
    session: Optional[ClientSession]

    def _init_(self, app: "Application", *_: list, **__: dict):
        self.session = None

    async def connect(self, *_: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.logger.info("JService is ready")

    async def disconnect(self, *_: "Application"):
        await self.session.close()
        self.logger.info("JService is closed")

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def get_random_questions(self, count: int) -> list:
        method = "random/"
        url = self._build_query(API_PATH, method, {"count": count})
        async with self.session.get(url) as resp:
            return await resp.json()

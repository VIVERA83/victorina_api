""""Модуль описывающий сервисы по работе с данными."""
from typing import TYPE_CHECKING

from store.database.database import Database
from store.jservice.accessor import JServiceAccessor
from store.question.manager import QuestionManager
from store.victorina.accessor import VictorinaAccessor

if TYPE_CHECKING:
    from app.core.app import Application


class Store:
    """Store, сервис данных и работы с ним.

    Инициализация источников данных."""

    def __init__(self, app: "Application"):
        self.j_service = JServiceAccessor(app)
        self.victorina = VictorinaAccessor(app)
        self.question_manager = QuestionManager(app)


def setup_store(app: "Application"):
    """Настраивая подключение и отключение хранилищ.

    Здесь мы сообщаем приложению, о базах базы данных и других источнгиков данных
    которые мы запускаем при запуске приложения, и как их отключить..
    """
    app.database = Database(app)
    app.store = Store(app)

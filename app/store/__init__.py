from typing import TYPE_CHECKING

from store.database.database import Database
from store.jservice.accessor import JServiceAccessor
from store.victorina.accessor import VictorinaAccessor
from store.question.manager import QuestionManager

if TYPE_CHECKING:
    from app.core.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.j_service = JServiceAccessor(app)
        self.victorina = VictorinaAccessor(app)
        self.question_manager = QuestionManager(app)


def setup_store(app: "Application"):
    """
    Configuring the connection and disconnection of storages that need to
    start with the application, here we tell the application which
    databases we launch at the start of the application and how to disable them
    """
    app.database = Database(app)
    app.store = Store(app)

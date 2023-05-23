import asyncio
from asyncio import CancelledError, Lock, Queue, Task
from typing import TYPE_CHECKING, Optional

from base.base_accessor import BaseAccessor
from base.utils import before_execution

from victorina.schemes import QuestionSchema

if TYPE_CHECKING:
    from core.app import Application


class QuestionManager(BaseAccessor):
    """Сервис обработки логики выдачи вопросов.

    Сервис выполняет"""

    tasks: Optional[Queue[int]] = None
    results: Optional[Queue[list]] = None
    is_running: Optional[bool] = None
    poll: Optional[Task] = None
    lock: Optional[Lock] = None

    def _init_(self, app: "Application", *_: list, **__: dict):
        """Дополнительные настройки."""
        # оборачиваем make_questions, теперь нам не страшныц разрывы и БД
        #  если связь потерена то в течении 15 сикунд будут пытаться потключиться к БД.
        self.make_questions = before_execution(
            total_timeout=15, fix_error=self.app.database.connect
        )(self.make_questions)

    async def connect(self, *_: "Application"):
        """Запуск poller."""
        self.is_running = True
        self.lock = Lock()
        self.tasks = Queue()
        self.results = Queue()
        self.results.put_nowait([])
        self.poll = asyncio.create_task(self.poller())
        self.logger.info(f"{self.__class__.__name__} is ready")

    async def disconnect(self, *_: "Application"):
        """Остановка poller`a."""
        self.is_running = False
        self.poll.cancel()
        await self.poll
        self.logger.info(f"{self.__class__.__name__} is close")

    async def get_questions(self, count: int) -> list:
        """Получить вопросы из очереди готовых результаттов."""
        self.tasks.put_nowait(count)
        try:
            return await self.results.get()
        except CancelledError:
            self.logger.warning(f"{self.__class__.__name__}.get_questions cancelled...")

    async def poller(self):
        """Poller - обрабатывает запросы из очереди tasks (Запросы на получения) и результаты складывает
        в очередь `results`"""
        while self.is_running:
            try:
                task = await self.tasks.get()
                results = await self.make_questions(task) or []
                await self.results.put(results)
            except CancelledError:
                self.logger.debug(f"{self.__class__.__name__}.poller cancelled...")

    async def make_questions(self, count: int) -> list:
        """Создать вопросы.

        Генерирует заданное количество вопросов которые еще не встречаются в базе данных.
        """
        questions = []
        while self.is_running and (count - len(questions)):
            count -= len(questions)
            question_ids, temp_result = await self.get_random_questions(count)
            # Проверка вопросов на то что они не повторяются в БД и добавление в БД новых вопросов
            async with self.lock:
                questions.extend(
                    await self.delete_repetitions([*question_ids, 71311], temp_result)
                )
                # добавляем вопросы в БД
                await self.app.store.victorina.add_questions(questions)

        return questions

    async def delete_repetitions(
        self, question_ids: list[int], questions: list[QuestionSchema]
    ) -> list[QuestionSchema]:
        """Удаляет повторяющиеся вопросы.

        Вспомогательная функция, для `make_questions`"""
        replay_questions = await self.app.store.victorina.get_questions_by_ids(
            question_ids
        )
        return [
            question for question in questions if question.id not in replay_questions
        ]

    async def get_random_questions(
        self, count
    ) -> (list[int], list[QuestionSchema],):
        """Генерирует заданное количество случайных вопросов."""
        questions = []
        questions_ids = []
        for data in await self.app.store.j_service.get_random_questions(count):
            question = QuestionSchema.parse_obj(data)
            questions.append(question)
            questions_ids.append(question.id)
        return questions_ids, questions

import asyncio
from asyncio import Queue, Task, CancelledError, Lock
from typing import TYPE_CHECKING, Optional

from base.base_accessor import BaseAccessor
from base.utils import before_execution
from victorina.schemes import QuestionSchema

if TYPE_CHECKING:
    from core.app import Application


class QuestionManager(BaseAccessor):
    tasks: Optional[Queue[int]] = None
    results: Optional[Queue[list]] = None
    is_running: Optional[bool] = None
    poll: Optional[Task] = None
    lock: Optional[Lock] = None

    async def connect(self, *_: "Application"):
        self.is_running = True
        self.lock = Lock()
        self.tasks = Queue()
        self.results = Queue()
        self.results.put_nowait([])
        self.poll = asyncio.create_task(self.poller())
        self.logger.info(f"{self.__class__.__name__} is ready")

    async def disconnect(self, *_: "Application"):
        self.is_running = False
        self.poll.cancel()
        await self.poll
        self.logger.info(f"{self.__class__.__name__} is close")

    async def get_questions(self, count: int) -> list:
        self.tasks.put_nowait(count)
        try:
            return await self.results.get()
        except CancelledError:
            self.logger.warning(f"{self.__class__.__name__}.get_questions cancelled...")

    async def poller(self):
        while self.is_running:
            try:
                task = await self.tasks.get()
                results = await self.make_questions(task)
                await self.results.put(results)
            except CancelledError:
                self.logger.debug(f"{self.__class__.__name__}.poller cancelled...")

    @before_execution(5)
    async def make_questions(self, count: int) -> list:
        questions = []
        while self.is_running and (count - len(questions)):
            count -= len(questions)
            question_ids, temp_result = await self.get_random_questions(count)
            # Проверка вопросов на то что они не повторяются в БД и добавление в БД новых вопросов
            async with self.lock:
                questions.extend(await self.delete_repetitions([*question_ids, 71311], temp_result))
                # добавляем вопросы в БД
                await self.app.store.victorina.add_questions(questions)
        return questions

    async def delete_repetitions(self,
                                 question_ids: list[int],
                                 questions: list[QuestionSchema]) -> list[QuestionSchema]:

        replay_questions = await self.app.store.victorina.get_questions_by_ids(question_ids)
        return [question for question in questions if question.id not in replay_questions]

    async def get_random_questions(self, count) -> (list[int], list[QuestionSchema],):
        questions = []
        questions_ids = []
        for data in await self.app.store.j_service.get_random_questions(count):
            question = QuestionSchema.parse_obj(data)
            questions.append(question)
            questions_ids.append(question.id)
        return questions_ids, questions

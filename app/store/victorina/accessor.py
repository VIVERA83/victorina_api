from typing import Optional

from base.base_accessor import BaseAccessor
from sqlalchemy import insert, select

from victorina.models import QuestionModel
from victorina.schemes import QuestionSchema


class VictorinaAccessor(BaseAccessor):
    async def get_questions_by_ids(
        self, ids: list[int]
    ) -> Optional[list[QuestionModel]]:
        async with self.app.database.session.begin().session as session:
            stmt = select(QuestionModel).where(QuestionModel.id.in_(ids))
            result = await session.execute(stmt)
            return result.unique().scalars().all()  # noqa

    async def add_questions(
        self, questions: list[QuestionSchema]
    ) -> list[QuestionModel]:
        async with self.app.database.session.begin().session as session:
            stmt = (
                insert(QuestionModel)
                .values([question.dict() for question in questions])
                .returning(QuestionModel)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.fetchall()  # noqa

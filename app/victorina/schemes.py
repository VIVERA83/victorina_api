"""Schemas сервиса Victorina."""
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field

query_number: int = Query(
    description="Количество возвращаемых ответов."
    "ограничение не более 100 за запрос.",
    ge=1,
    lt=100,
    title="Количество ответов",
    example=2,
)


class QuestionSchema(BaseModel):
    id: int = Field(
        description="уникальный `id` вопроса, задается автоматически",
        title="Id вопроса",
    )
    question: str = Field(description="Развернутое описание вопроса", title="Вопрос")
    answer: str = Field(description="Ответ на вопрос", title="Ответ")
    created_at: datetime = Field(description="Дата созжания вопроса", title="Дата")

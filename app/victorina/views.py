from typing import Any

from core.components import Request
from fastapi import APIRouter

from victorina.schemes import QuestionSchema, query_number

victorina_route = APIRouter()


@victorina_route.get(
    "/question",
    summary="Получить вопрос",
    description="Метод вернет вопросы в количестве указанном в параметре `questions_num`, "
    "Если запрос делается впервые будет возвращен пустой объект `Question`",
    response_description="Список воросов",
    tags=["GET"],
    response_model=list[QuestionSchema] | None,
)
async def test(request: "Request", questions_num: int = query_number) -> Any:
    """ "Получить вопрос."""
    return await request.app.store.question_manager.get_questions(questions_num)

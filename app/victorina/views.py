from typing import Optional, Any

from fastapi import APIRouter

from core.components import Request

from victorina.schemes import query_number, QuestionSchema

victorina_route = APIRouter()


@victorina_route.get("/question",
                     summary="Получить вопрос",
                     description=f"Метод вернет вопросы в количестве указанном в параметре `questions_num`, "
                                 f"Если запрос делается впервые будет возвращен пустой объект `Question`",
                     response_description="Список воросов",
                     tags=["GET"],
                     response_model=list[QuestionSchema] | None,
                     )
async def test(request: "Request", questions_num: int = query_number) -> Any:
    return await request.app.store.question_manager.get_questions(questions_num)

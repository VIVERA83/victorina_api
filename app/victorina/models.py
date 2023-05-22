from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped

from store.database.database import Base
from datetime import datetime


@dataclass
class QuestionModel(Base):
    __tablename__ = "questions"  # noqa
    id: Mapped[int] = Column(Integer, primary_key=True)
    question: Mapped[str] = Column(String(length=500), nullable=False)
    answer: Mapped[str] = Column(String(length=100), nullable=False)
    created_at: Mapped[datetime] = Column(type_=TIMESTAMP(timezone=True), nullable=False)

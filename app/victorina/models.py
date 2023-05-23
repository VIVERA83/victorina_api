"""Модели сервиса Victorina"""
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import Mapped
from store.database.database import Base


@dataclass
class QuestionModel(Base):
    """Question model."""

    __tablename__ = "questions"  # noqa
    id: Mapped[int] = Column(Integer, primary_key=True)
    question: Mapped[str] = Column(String(length=500), nullable=False)
    answer: Mapped[str] = Column(String(length=100), nullable=False)
    created_at: Mapped[datetime] = Column(
        type_=TIMESTAMP(timezone=True), nullable=False
    )

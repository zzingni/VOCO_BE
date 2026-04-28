from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, default=1)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    stt_text = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
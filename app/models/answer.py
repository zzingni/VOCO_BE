from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy.orm import relationship


class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("member.id"))
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    interview_id = Column(Integer, ForeignKey("interview.id"), nullable=False)

    stt_text = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

    interview = relationship("Interview", back_populates="answers")
    question = relationship("Question")
    member = relationship("Member", back_populates="answers")
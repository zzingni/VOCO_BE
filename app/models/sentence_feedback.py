from sqlalchemy import Column, Integer, Text, DateTime
from app.db.database import Base
from datetime import datetime


class SentenceFeedback(Base):
    __tablename__ = "sentence_feedback"

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
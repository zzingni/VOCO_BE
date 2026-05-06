from sqlalchemy import Column, Integer, DECIMAL, DateTime
from app.db.database import Base
from datetime import datetime


class VoiceFeedback(Base):
    __tablename__ = "voice_feedback"

    voice_feedback_id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, nullable=False)

    speed = Column(Integer, nullable=False)
    pitch = Column(Integer, nullable=False)

    energy = Column(DECIMAL(10, 4), nullable=False)

    score = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
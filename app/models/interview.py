from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Interview(Base):
    __tablename__ = "interview"

    user_id = Column(Integer, default=1)
    id = Column(Integer, primary_key=True, index=True)
    interview_date = Column(TIMESTAMP, server_default=func.now())

    # Answer 와 1:N 관계
    answers = relationship("Answer", back_populates="interview")
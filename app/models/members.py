from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base


class Member(Base):

    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=True)
    age = Column(Integer, nullable=True)
    kakao_access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    birth_date = Column(Date, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)

    interviews = relationship("Interview", back_populates="member")
    answers = relationship("Answer", back_populates="member")
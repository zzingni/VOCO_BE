from sqlalchemy import Column, Integer, String, Boolean, Date, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base

class Member(Base):

    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    kakao_id = Column(String(255), unique=True, index=True, nullable=True)
    nickname = Column(String(50), nullable=False)
    kakao_access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)

    interviews = relationship("Interview", back_populates="member")
    answers = relationship("Answer", back_populates="member")

    posts = relationship("Post", back_populates="member")
    comments = relationship("Comment", back_populates="member")
    resume = relationship("Resume", back_populates="member",uselist=False)
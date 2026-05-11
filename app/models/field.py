from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Field(Base):
    __tablename__ = "field"

    id = Column(Integer, primary_key=True, index=True)

    main_category = Column(String(50), nullable=False)
    sub_category = Column(String(100), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(Boolean, default=True)

    # Question 테이블과 관계 설정
    questions = relationship("Question", back_populates="field")
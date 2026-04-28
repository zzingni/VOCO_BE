from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.database import Base
from sqlalchemy.orm import relationship

field = relationship("Field", back_populates="questions")

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("field.id"), nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(Boolean, default=True)
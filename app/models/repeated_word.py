from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base


class RepeatedWord(Base):
    __tablename__ = "repeated_word"

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("answer.id", ondelete="CASCADE"), nullable=False)
    word = Column(String(100), nullable=False)
    word_count = Column(Integer, nullable=False)
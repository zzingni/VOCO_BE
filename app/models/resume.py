from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.database import Base


class Resume(Base):

    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, index=True)

    member_id = Column(
        Integer,
        ForeignKey("member.id"),
        nullable=False,
        unique=True
    )

    personality = Column(Text, nullable=False)
    motivation = Column(Text, nullable=False)
    problem_experience = Column(Text, nullable=False)
    aspiration = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    member = relationship("Member", back_populates="resume")
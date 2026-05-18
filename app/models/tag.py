from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Tag(Base):

    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    status =  Column(String(20), default="ACTIVE")

    posts = relationship("Post", back_populates="tag")
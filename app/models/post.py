from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Post(Base):

    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.tag_id"), nullable=False)

    title =  Column(String(255), nullable=False)
    content =  Column(Text, nullable=False)
    image_url =  Column(Text, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = deleted_at = Column(TIMESTAMP, nullable=True)

    status =  Column(String(20), default="ACTIVE")

    member = relationship("Member", back_populates="posts")
    tag = relationship("Tag", back_populates="posts")
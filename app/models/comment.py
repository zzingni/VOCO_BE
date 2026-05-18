from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Comment(Base):

    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.post_id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.comment_id"), nullable=True)

    content =  Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
    status = Column(String(20), nullable=False, default="ACTIVE")

    member = relationship("Member", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    parent  = relationship("Comment",  remote_side=[comment_id], backref="replies")
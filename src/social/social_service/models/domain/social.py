"""
Модели данных для социального взаимодействия.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.social.social_service.database import Base


class Subscription(Base):
    """
    Модель для подписок пользователей друг на друга.
    """
    __tablename__ = "subscription"
    __table_args__ = {"schema": "social_service_schema"}

    subscription_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    follower_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    followed_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Subscription {self.follower_id} -> {self.followed_id}>"


class Comment(Base):
    """
    Модель для комментариев к источникам.
    """
    __tablename__ = "comment"
    __table_args__ = {"schema": "social_service_schema"}

    comment_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("social_service_schema.comment.comment_id"), nullable=True)
    content = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    # Связи
    replies = relationship("Comment",
                           remote_side=[comment_id],
                           backref=("parent"),
                           cascade="all, delete-orphan")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Comment {self.comment_id} by {self.user_id}>"
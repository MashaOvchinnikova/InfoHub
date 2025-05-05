"""
Схемы Pydantic для валидации данных социального взаимодействия.
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class SubscriptionBase(BaseModel):
    """Базовая схема для подписки."""
    followed_id: uuid.UUID


class SubscriptionCreate(SubscriptionBase):
    """Схема для создания подписки."""
    follower_id: uuid.UUID


class Subscription(SubscriptionBase):
    """Схема для полного представления подписки."""
    subscription_id: uuid.UUID
    follower_id: uuid.UUID
    created_date: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    """Базовая схема для комментария."""
    content: str = Field(..., min_length=1)
    parent_comment_id: Optional[uuid.UUID] = None


class CommentCreate(CommentBase):
    """Схема для создания комментария."""
    user_id: uuid.UUID
    source_id: uuid.UUID


class CommentUpdate(BaseModel):
    """Схема для обновления комментария."""
    content: str = Field(..., min_length=1)


class Comment(CommentBase):
    """Схема для полного представления комментария."""
    comment_id: uuid.UUID
    user_id: uuid.UUID
    source_id: uuid.UUID
    created_date: datetime
    updated_date: datetime
    is_deleted: bool

    class Config:
        from_attributes = True


class CommentWithReplies(Comment):
    """Схема для представления комментария с ответами."""
    replies: List["CommentWithReplies"] = []
    user_name: Optional[str] = None  # Имя пользователя для отображения

    class Config:
        from_attributes = True


class FeedItem(BaseModel):
    """Схема для элемента ленты активности."""
    activity_id: uuid.UUID
    user_id: uuid.UUID
    user_name: str
    activity_type: str
    entity_type: str
    entity_id: uuid.UUID
    entity_title: Optional[str] = None
    entity_url: Optional[str] = None
    created_date: datetime

    class Config:
        from_attributes = True

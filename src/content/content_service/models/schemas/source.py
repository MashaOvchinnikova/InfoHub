"""
Схемы Pydantic для валидации данных источников.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class ContentType(str, Enum):
    """Типы контента источников."""
    ARTICLE = "article"
    VIDEO = "video"
    BOOK = "book"
    PODCAST = "podcast"
    COURSE = "course"
    OTHER = "other"


class TagBase(BaseModel):
    """Базовая схема для тега."""
    name: str
    description: Optional[str] = None


class TagCreate(TagBase):
    """Схема для создания тега."""
    pass


class Tag(TagBase):
    """Схема для полного представления тега."""
    tag_id: uuid.UUID
    usage_count: int

    class Config:
        from_attributes = True


class RatingBase(BaseModel):
    """Базовая схема для оценки."""
    value: int = Field(..., ge=1, le=5)  # значение от 1 до 5


class RatingCreate(RatingBase):
    """Схема для создания оценки."""
    source_id: uuid.UUID
    user_id: uuid.UUID


class Rating(RatingBase):
    """Схема для полного представления оценки."""
    rating_id: uuid.UUID
    source_id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    """Базовая схема для источника."""
    title: str
    url: HttpUrl
    description: Optional[str] = None
    thumbnail_url: Optional[HttpUrl] = None
    content_type: ContentType
    publication_date: Optional[datetime] = None


class SourceCreate(SourceBase):
    """Схема для создания источника."""
    added_by: Optional[uuid.UUID] = None
    tags: List[str] = []  # список имен тегов


class SourceUpdate(BaseModel):
    """Схема для обновления источника."""
    title: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    thumbnail_url: Optional[HttpUrl] = None
    content_type: Optional[ContentType] = None
    publication_date: Optional[datetime] = None
    is_verified: Optional[bool] = None
    is_recommended: Optional[bool] = None


class SourceResponse(SourceBase):
    """Схема для полного представления источника."""
    source_id: uuid.UUID
    added_date: datetime
    added_by: Optional[uuid.UUID] = None
    is_verified: bool
    is_recommended: bool
    avg_rating: float
    tags: List[Tag] = []

    class Config:
        from_attributes = True
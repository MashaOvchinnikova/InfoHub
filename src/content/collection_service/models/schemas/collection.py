"""
Схемы Pydantic для валидации данных коллекций.
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class CollectionSourceBase(BaseModel):
    """Базовая схема для связи коллекции и источника."""
    source_id: uuid.UUID
    note: Optional[str] = None


class CollectionSourceCreate(CollectionSourceBase):
    """Схема для добавления источника в коллекцию."""
    pass


class CollectionSource(CollectionSourceBase):
    """Схема для полного представления источника в коллекции."""
    collection_source_id: uuid.UUID
    collection_id: uuid.UUID
    added_date: datetime

    class Config:
        from_attributes = True


class CollectionBase(BaseModel):
    """Базовая схема для коллекции."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: bool = True


class CollectionCreate(CollectionBase):
    """Схема для создания коллекции."""
    user_id: uuid.UUID


class CollectionUpdate(BaseModel):
    """Схема для обновления коллекции."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: Optional[bool] = None


class Collection(CollectionBase):
    """Схема для полного представления коллекции."""
    collection_id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime
    updated_date: datetime
    sources: List[CollectionSource] = []

    class Config:
        from_attributes = True


class CollectionWithSourceDetails(Collection):
    """Схема для представления коллекции с детальной информацией об источниках."""
    sources: List["SourceInCollection"] = []

    class Config:
        from_attributes = True


class SourceInCollection(BaseModel):
    """Схема для представления источника в коллекции с дополнительной информацией."""
    collection_source_id: uuid.UUID
    source_id: uuid.UUID
    title: str
    url: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    content_type: str
    added_date: datetime
    note: Optional[str] = None

    class Config:
        from_attributes = True

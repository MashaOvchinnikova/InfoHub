"""
Модели данных для информационных источников.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.content.content_service.database import Base


class ContentType(str, Enum):
    """Типы контента источников."""
    ARTICLE = "article"
    VIDEO = "video"
    BOOK = "book"
    PODCAST = "podcast"
    COURSE = "course"
    OTHER = "other"


class Source(Base):
    """
    Модель для информационных источников.
    """
    __tablename__ = "source"

    source_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    content_type = Column(String, nullable=False)
    publication_date = Column(DateTime, nullable=True)
    added_date = Column(DateTime, default=datetime.utcnow)
    added_by = Column(UUID(as_uuid=True), nullable=True)  # ID пользователя
    is_verified = Column(Boolean, default=False)
    is_recommended = Column(Boolean, default=False)
    avg_rating = Column(Float, default=0.0)

    # Связи
    tags = relationship("SourceTag", back_populates="source")
    ratings = relationship("Rating", back_populates="source")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Source {self.title}>"


class Tag(Base):
    """
    Модель для тегов источников.
    """
    __tablename__ = "tag"

    tag_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True, unique=True)
    description = Column(String, nullable=True)
    usage_count = Column(Integer, default=0)

    # Связи
    sources = relationship("SourceTag", back_populates="tag")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Tag {self.name}>"


class SourceTag(Base):
    """
    Связующая модель между источниками и тегами.
    """
    __tablename__ = "source_tag"

    source_tag_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("source.source_id"), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tag.tag_id"), nullable=False)

    # Связи
    source = relationship("Source", back_populates="tags")
    tag = relationship("Tag", back_populates="sources")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<SourceTag {self.source_id}:{self.tag_id}>"


class Rating(Base):
    """
    Модель для оценок источников пользователями.
    """
    __tablename__ = "rating"

    rating_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    source_id = Column(UUID(as_uuid=True), ForeignKey("source.source_id"), nullable=False)
    value = Column(Integer, nullable=False)  # например от 1 до 5
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    source = relationship("Source", back_populates="ratings")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Rating {self.value} for {self.source_id} by {self.user_id}>"

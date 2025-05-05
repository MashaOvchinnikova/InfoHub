"""
Модели данных для коллекций пользователей.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.content.collection_service.database import Base


class Collection(Base):
    """
    Модель для коллекций пользователей.
    """
    __tablename__ = "collection"
    __table_args__ = {"schema": "collection_service_schema"}

    collection_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_public = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Связи
    sources = relationship("CollectionSource", back_populates="collection")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Collection {self.name} by {self.user_id}>"


class CollectionSource(Base):
    """
    Связующая модель между коллекциями и источниками.
    """
    __tablename__ = "collection_source"
    __table_args__ = {"schema": "collection_service_schema"}


    collection_source_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    collection_id = Column(UUID(as_uuid=True), ForeignKey("collection_service_schema.collection.collection_id"), nullable=False)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    added_date = Column(DateTime, default=datetime.utcnow)
    note = Column(Text, nullable=True)

    # Связи
    collection = relationship("Collection", back_populates="sources")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<CollectionSource {self.collection_id}:{self.source_id}>"
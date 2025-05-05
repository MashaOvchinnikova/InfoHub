"""
Модели данных для поискового индекса и сохранения поисковых запросов.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Text, JSON, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from src.discovery.search_service.database import Base


class SearchIndex(Base):
    """
    Модель поискового индекса, хранящая индексированные данные источников.
    Используется как кэш данных из source, tag, и других таблиц для быстрого поиска.
    """
    __tablename__ = "search_index"
    __table_args__ = {"schema": "search_service_schema"}

    # Основные поля
    index_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), index=True, nullable=False)  # Ссылка на ID оригинального источника

    # Поля для поиска
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    url = Column(String, nullable=False)
    content_type = Column(String, nullable=False, index=True)  # тип контента (статья, видео, книга и т.д.)

    # Поля для фильтрации и сортировки
    publication_date = Column(DateTime, nullable=True, index=True)
    added_date = Column(DateTime, default=datetime.utcnow, index=True)
    avg_rating = Column(Float, default=0.0, index=True)
    is_verified = Column(Boolean, default=False, index=True)
    is_recommended = Column(Boolean, default=False, index=True)

    # Денормализованные поля для оптимизации поиска
    tags = Column(ARRAY(String), nullable=True)
    tag_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    interests = Column(ARRAY(String), nullable=True)
    interest_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    added_by_username = Column(String, nullable=True)

    # Метаданные для ранжирования
    popularity_score = Column(Float, default=0.0, index=True)
    relevance_score = Column(Float, default=0.0)

    # Дополнительные метаданные
    thumbnail_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Дополнительные данные для полнотекстового поиска
    search_vector = Column(Text, nullable=True)  # Для хранения подготовленного текста для поиска

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<SearchIndex {self.source_id}: {self.title}>"


class SearchQuery(Base):
    """
    Модель для хранения поисковых запросов пользователей.
    Используется для аналитики и рекомендаций популярных запросов.
    """
    __tablename__ = "search_query"
    __table_args__ = {"schema": "search_service_schema"}


    query_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=True)  # Может быть NULL для анонимных запросов

    query_text = Column(String, nullable=False, index=True)
    query_params = Column(JSON, nullable=True)  # Дополнительные параметры запроса (фильтры и т.д.)

    results_count = Column(Integer, default=0)  # Количество найденных результатов
    execution_time_ms = Column(Integer, nullable=True)  # Время выполнения запроса

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String, nullable=True)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<SearchQuery {self.query_text}>"


class PopularSearch(Base):
    """
    Модель для хранения популярных поисковых запросов.
    Аггрегированные данные для быстрого доступа.
    """
    __tablename__ = "popular_search"
    __table_args__ = {"schema": "search_service_schema"}


    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    query_text = Column(String, unique=True, nullable=False, index=True)

    count = Column(Integer, default=1, index=True)
    last_searched_at = Column(DateTime, default=datetime.utcnow)

    # Периоды популярности
    daily_count = Column(Integer, default=0)
    weekly_count = Column(Integer, default=0)
    monthly_count = Column(Integer, default=0)

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<PopularSearch {self.query_text}: {self.count}>"


class UserRecentSearch(Base):
    """
    Модель для хранения недавних поисковых запросов пользователя.
    """
    __tablename__ = "user_recent_search"
    __table_args__ = {"schema": "search_service_schema"}


    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    query_text = Column(String, nullable=False)
    query_params = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<UserRecentSearch {self.user_id}: {self.query_text}>"


class SearchSuggestion(Base):
    """
    Модель для хранения подсказок при автодополнении поиска.
    """
    __tablename__ = "search_suggestion"
    __table_args__ = {"schema": "search_service_schema"}


    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    text = Column(String, unique=True, nullable=False, index=True)

    type = Column(String, nullable=False, index=True)  # tag, interest, title, etc.
    source_id = Column(UUID(as_uuid=True), nullable=True)  # Если подсказка связана с конкретным источником

    weight = Column(Float, default=1.0, index=True)  # Вес для сортировки подсказок
    usage_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<SearchSuggestion {self.text} ({self.type})>"
"""
Модели данных для таблиц рекомендаций.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, DateTime, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID, ARRAY

from src.discovery.recommendation_service.database import Base


class RecommendationType(str, Enum):
    """Типы рекомендаций."""
    PERSONALIZED = "personalized"
    SIMILAR = "similar"
    POPULAR = "popular"
    TRENDING = "trending"
    INTEREST_BASED = "interest_based"


class UserRecommendation(Base):
    """
    Модель для хранения персонализированных рекомендаций пользователям.
    """
    __tablename__ = "user_recommendations"

    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    source_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Тип рекомендации и уровень релевантности
    recommendation_type = Column(String, nullable=False)
    relevance_score = Column(Float, nullable=False, default=0.0)
    explanation = Column(String(255), nullable=True)

    # Интересы, на основе которых сделана рекомендация
    interests = Column(ARRAY(UUID(as_uuid=True)), nullable=True)

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_shown = Column(Integer, default=0)  # Счетчик показов
    is_clicked = Column(Integer, default=0)  # Счетчик кликов

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<UserRecommendation {self.user_id} - {self.source_id}>"


class SimilarSource(Base):
    """
    Модель для хранения похожих источников.
    """
    __tablename__ = "similar_sources"

    similar_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    similar_source_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Оценка схожести и причина
    similarity_score = Column(Float, nullable=False)
    similarity_reasons = Column(JSON, nullable=True)  # Например, общие теги, тематика и т.д.

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<SimilarSource {self.source_id} - {self.similar_source_id}>"


class PopularSource(Base):
    """
    Модель для хранения популярных источников.
    """
    __tablename__ = "popular_sources"

    popular_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Метрики популярности
    view_count = Column(Integer, default=0)
    save_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    rating_avg = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)

    # Общий рейтинг популярности
    popularity_score = Column(Float, default=0.0)

    # Период и категория
    time_period = Column(String(20), nullable=False)  # 'daily', 'weekly', 'monthly', 'all_time'
    category = Column(String(50), nullable=True)  # Опциональная категория

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<PopularSource {self.source_id} ({self.time_period})>"


class InterestRecommendation(Base):
    """
    Модель для хранения рекомендаций по интересам.
    """
    __tablename__ = "interest_recommendations"

    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    interest_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    source_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Оценка релевантности
    relevance_score = Column(Float, nullable=False, default=0.0)

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<InterestRecommendation {self.interest_id} - {self.source_id}>"


class UserPreference(Base):
    """
    Модель для хранения предпочтений пользователя (для аналитики рекомендаций).
    """
    __tablename__ = "user_preferences"

    preference_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)

    # Предпочтения по источникам и интересам
    liked_sources = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    disliked_sources = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    viewed_sources = Column(JSON, nullable=True)  # {source_id: view_count}
    interest_weights = Column(JSON, nullable=True)  # {interest_id: weight}

    # Предпочтения по типам контента
    content_type_preferences = Column(JSON, nullable=True)  # {content_type: weight}

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<UserPreference {self.user_id}>"
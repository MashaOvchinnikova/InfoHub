"""
Схемы Pydantic для валидации данных при работе с рекомендациями.
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

from pydantic import BaseModel, Field, validator


class RecommendationBase(BaseModel):
    """Базовая схема для рекомендации."""
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    recommendation_type: str


class UserRecommendationCreate(RecommendationBase):
    """Схема для создания персонализированной рекомендации."""
    user_id: uuid.UUID
    source_id: uuid.UUID
    explanation: Optional[str] = None
    interests: Optional[List[uuid.UUID]] = None


class UserRecommendationResponse(RecommendationBase):
    """Схема для ответа с данными персонализированной рекомендации."""
    recommendation_id: uuid.UUID
    user_id: uuid.UUID
    source_id: uuid.UUID
    explanation: Optional[str] = None
    interests: Optional[List[uuid.UUID]] = None
    created_at: datetime
    updated_at: datetime
    is_shown: int
    is_clicked: int

    class Config:
        from_attributes = True


class SimilarSourceBase(BaseModel):
    """Базовая схема для похожего источника."""
    source_id: uuid.UUID
    similar_source_id: uuid.UUID
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    similarity_reasons: Optional[Dict[str, Any]] = None


class SimilarSourceCreate(SimilarSourceBase):
    """Схема для создания похожего источника."""
    pass


class SimilarSourceResponse(SimilarSourceBase):
    """Схема для ответа с данными похожего источника."""
    similar_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PopularSourceBase(BaseModel):
    """Базовая схема для популярного источника."""
    source_id: uuid.UUID
    time_period: str = Field(..., description="Период популярности: daily, weekly, monthly, all_time")
    category: Optional[str] = None
    popularity_score: float = Field(..., ge=0.0)

    # Детальные метрики популярности
    view_count: int = 0
    save_count: int = 0
    share_count: int = 0
    rating_avg: float = 0.0
    rating_count: int = 0


class PopularSourceCreate(PopularSourceBase):
    """Схема для создания популярного источника."""
    pass


class PopularSourceResponse(PopularSourceBase):
    """Схема для ответа с данными популярного источника."""
    popular_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InterestRecommendationBase(BaseModel):
    """Базовая схема для рекомендации по интересу."""
    interest_id: uuid.UUID
    source_id: uuid.UUID
    relevance_score: float = Field(..., ge=0.0, le=1.0)


class InterestRecommendationCreate(InterestRecommendationBase):
    """Схема для создания рекомендации по интересу."""
    pass


class InterestRecommendationResponse(InterestRecommendationBase):
    """Схема для ответа с данными рекомендации по интересу."""
    recommendation_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPreferenceBase(BaseModel):
    """Базовая схема для предпочтений пользователя."""
    user_id: uuid.UUID
    liked_sources: Optional[List[uuid.UUID]] = None
    disliked_sources: Optional[List[uuid.UUID]] = None
    viewed_sources: Optional[Dict[str, int]] = None
    interest_weights: Optional[Dict[str, float]] = None
    content_type_preferences: Optional[Dict[str, float]] = None


class UserPreferenceCreate(UserPreferenceBase):
    """Схема для создания предпочтений пользователя."""
    pass


class UserPreferenceUpdate(BaseModel):
    """Схема для обновления предпочтений пользователя."""
    liked_sources: Optional[List[uuid.UUID]] = None
    disliked_sources: Optional[List[uuid.UUID]] = None
    viewed_sources: Optional[Dict[str, int]] = None
    interest_weights: Optional[Dict[str, float]] = None
    content_type_preferences: Optional[Dict[str, float]] = None


class UserPreferenceResponse(UserPreferenceBase):
    """Схема для ответа с данными предпочтений пользователя."""
    preference_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    """Схема для запроса рекомендаций."""
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    exclude_ids: Optional[List[uuid.UUID]] = None
    include_viewed: bool = False


class SourceBasicInfo(BaseModel):
    """Базовая информация об источнике для рекомендаций."""
    source_id: uuid.UUID
    title: str
    description: Optional[str] = None
    url: str
    thumbnail_url: Optional[str] = None
    content_type: str
    avg_rating: float

    class Config:
        from_attributes = True


class RecommendationSourceResponse(BaseModel):
    """Схема для ответа с рекомендацией источника."""
    source: SourceBasicInfo
    relevance_score: float
    recommendation_type: str
    explanation: Optional[str] = None
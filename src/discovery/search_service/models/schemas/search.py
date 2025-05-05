"""
Схемы Pydantic для валидации данных при работе с поисковым индексом.
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum

from pydantic import BaseModel, Field, HttpUrl, validator, root_validator


class ContentType(str, Enum):
    """Перечисление типов контента."""
    ARTICLE = "article"
    VIDEO = "video"
    BOOK = "book"
    PODCAST = "podcast"
    COURSE = "course"
    OTHER = "other"


class SuggestionType(str, Enum):
    """Перечисление типов поисковых подсказок."""
    TAG = "tag"
    INTEREST = "interest"
    TITLE = "title"
    SOURCE = "source"
    AUTHOR = "author"
    QUERY = "query"


class SortDirection(str, Enum):
    """Направление сортировки."""
    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    """Поля для сортировки результатов поиска."""
    RELEVANCE = "relevance"
    PUBLICATION_DATE = "publication_date"
    ADDED_DATE = "added_date"
    RATING = "avg_rating"
    POPULARITY = "popularity_score"


class SearchIndexBase(BaseModel):
    """Базовая схема для элемента поискового индекса."""
    title: str
    description: Optional[str] = None
    url: str
    content_type: ContentType

    publication_date: Optional[datetime] = None
    avg_rating: Optional[float] = 0.0
    is_verified: Optional[bool] = False
    is_recommended: Optional[bool] = False

    tags: Optional[List[str]] = []
    interests: Optional[List[str]] = []

    thumbnail_url: Optional[str] = None


class SearchIndexCreate(SearchIndexBase):
    """Схема для создания элемента поискового индекса."""
    source_id: uuid.UUID
    tag_ids: Optional[List[uuid.UUID]] = []
    interest_ids: Optional[List[uuid.UUID]] = []
    added_by_username: Optional[str] = None


class SearchIndexUpdate(BaseModel):
    """Схема для обновления элемента поискового индекса."""
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    content_type: Optional[ContentType] = None

    publication_date: Optional[datetime] = None
    avg_rating: Optional[float] = None
    is_verified: Optional[bool] = None
    is_recommended: Optional[bool] = None

    tags: Optional[List[str]] = None
    tag_ids: Optional[List[uuid.UUID]] = None
    interests: Optional[List[str]] = None
    interest_ids: Optional[List[uuid.UUID]] = None

    thumbnail_url: Optional[str] = None
    popularity_score: Optional[float] = None
    relevance_score: Optional[float] = None


class SearchIndexInDB(SearchIndexBase):
    """Схема для представления элемента поискового индекса из БД."""
    index_id: uuid.UUID
    source_id: uuid.UUID

    tag_ids: Optional[List[uuid.UUID]] = []
    interest_ids: Optional[List[uuid.UUID]] = []

    popularity_score: float = 0.0
    relevance_score: float = 0.0

    added_date: datetime
    added_by_username: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SearchIndexResponse(SearchIndexBase):
    """Схема для ответа с данными элемента поискового индекса."""
    index_id: uuid.UUID
    source_id: uuid.UUID

    popularity_score: float = 0.0
    relevance_score: float = 0.0

    added_date: datetime
    added_by_username: Optional[str] = None

    class Config:
        from_attributes = True


class SearchFilter(BaseModel):
    """Схема для фильтрации результатов поиска."""
    content_types: Optional[List[ContentType]] = None
    tags: Optional[List[str]] = None
    interests: Optional[List[str]] = None

    min_rating: Optional[float] = None
    is_verified: Optional[bool] = None
    is_recommended: Optional[bool] = None

    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @validator("min_rating")
    def validate_min_rating(cls, v):
        """Проверка минимального рейтинга."""
        if v is not None and (v < 0 or v > 5):
            raise ValueError("Минимальный рейтинг должен быть в диапазоне от 0 до 5")
        return v

    @validator("start_date", "end_date")
    def validate_dates(cls, v, values, **kwargs):
        """Проверка дат."""
        field_name = kwargs["field"]
        if field_name == "end_date" and v is not None:
            start_date = values.get("start_date")
            if start_date is not None and v < start_date:
                raise ValueError("Конечная дата не может быть раньше начальной")
        return v


class SearchSort(BaseModel):
    """Схема для сортировки результатов поиска."""
    field: SortField = SortField.RELEVANCE
    direction: SortDirection = SortDirection.DESC


class SearchQuery(BaseModel):
    """Схема для выполнения поискового запроса."""
    query: str
    filters: Optional[SearchFilter] = None
    sort: Optional[SearchSort] = None

    page: int = Field(1, gt=0)
    size: int = Field(10, gt=0, le=100)

    user_id: Optional[uuid.UUID] = None

    @validator("query")
    def validate_query(cls, v):
        """Проверка поискового запроса."""
        if len(v.strip()) < 1:
            raise ValueError("Поисковый запрос не может быть пустым")
        return v


class SearchResponse(BaseModel):
    """Схема для ответа на поисковый запрос."""
    results: List[SearchIndexResponse]
    total: int
    page: int
    size: int
    query: str
    execution_time_ms: Optional[int] = None


class SearchQueryRecord(BaseModel):
    """Схема для записи поискового запроса в историю."""
    query_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None

    query_text: str
    query_params: Optional[Dict[str, Any]] = None

    results_count: int = 0
    execution_time_ms: Optional[int] = None

    created_at: datetime
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True


class PopularSearchResponse(BaseModel):
    """Схема для ответа с популярными поисковыми запросами."""
    query_text: str
    count: int
    last_searched_at: datetime

    class Config:
        from_attributes = True


class UserRecentSearchResponse(BaseModel):
    """Схема для ответа с недавними поисковыми запросами пользователя."""
    id: uuid.UUID
    query_text: str
    query_params: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SuggestionCreate(BaseModel):
    """Схема для создания поисковой подсказки."""
    text: str
    type: SuggestionType
    source_id: Optional[uuid.UUID] = None
    weight: float = 1.0

    @validator("text")
    def validate_text(cls, v):
        """Проверка текста подсказки."""
        if len(v.strip()) < 1:
            raise ValueError("Текст подсказки не может быть пустым")
        return v


class SuggestionResponse(BaseModel):
    """Схема для ответа с поисковыми подсказками."""
    id: uuid.UUID
    text: str
    type: SuggestionType
    source_id: Optional[uuid.UUID] = None
    weight: float
    usage_count: int

    class Config:
        from_attributes = True


class SuggestionUpdate(BaseModel):
    """Схема для обновления поисковой подсказки."""
    text: Optional[str] = None
    type: Optional[SuggestionType] = None
    source_id: Optional[uuid.UUID] = None
    weight: Optional[float] = None
    usage_count: Optional[int] = None


class SuggestionQuery(BaseModel):
    """Схема для запроса поисковых подсказок."""
    prefix: str
    types: Optional[List[SuggestionType]] = None
    limit: int = Field(5, gt=0, le=20)

    @validator("prefix")
    def validate_prefix(cls, v):
        """Проверка префикса запроса."""
        if len(v.strip()) < 1:
            raise ValueError("Префикс запроса не может быть пустым")
        return v


class AdvancedSearchQuery(SearchQuery):
    """Схема для расширенного поискового запроса."""
    fuzzy_search: bool = False
    include_similar: bool = False
    boost_fields: Optional[Dict[str, float]] = None  # Например, {"title": 2.0, "description": 0.5}
    min_should_match: Optional[int] = None  # Минимальное количество совпадающих слов

    @root_validator
    def validate_advanced_query(cls, values):
        """Проверка расширенного поискового запроса."""
        boost_fields = values.get("boost_fields")
        if boost_fields:
            allowed_fields = ["title", "description", "tags", "interests"]
            for field in boost_fields:
                if field not in allowed_fields:
                    raise ValueError(f"Недопустимое поле для усиления: {field}")
        return values
"""
Схемы Pydantic для валидации данных при работе с сервисом парсинга.
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

from pydantic import BaseModel, Field, AnyUrl, validator


class TaskBase(BaseModel):
    """Базовая схема для задачи парсинга."""
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    url: AnyUrl
    task_type: str = Field(..., description="Тип задачи: single_url, website, rss, scheduled")
    params: Optional[Dict[str, Any]] = None


class TaskCreate(TaskBase):
    """Схема для создания задачи парсинга."""
    pass


class ScheduleParams(BaseModel):
    """Схема для параметров расписания задачи."""
    schedule_type: str = Field(..., description="Тип расписания: cron или interval")
    schedule_value: str = Field(..., description="Значение расписания")


class ScheduledTaskCreate(TaskCreate):
    """Схема для создания периодической задачи парсинга."""
    schedule: ScheduleParams


class TaskUpdate(BaseModel):
    """Схема для обновления задачи парсинга."""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    url: Optional[AnyUrl] = None
    params: Optional[Dict[str, Any]] = None


class TaskResponse(TaskBase):
    """Схема для ответа с данными задачи парсинга."""
    task_id: uuid.UUID
    status: str
    created_by: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    sources_found: int
    sources_created: int

    class Config:
        from_attributes = True


class ScheduledTaskResponse(TaskResponse):
    """Схема для ответа с данными периодической задачи парсинга."""
    scheduled_task_id: uuid.UUID
    schedule_type: str
    schedule_value: str
    is_active: bool
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None

    class Config:
        from_attributes = True


class ParsedSourceBase(BaseModel):
    """Базовая схема для распарсенного источника."""
    url: AnyUrl
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content: Optional[str] = None
    thumbnail_url: Optional[AnyUrl] = None
    content_type: Optional[str] = None
    publication_date: Optional[datetime] = None
    author: Optional[str] = None
    source_site: Optional[str] = None
    language: Optional[str] = None
    keywords: Optional[List[str]] = None


class ParsedSourceCreate(ParsedSourceBase):
    """Схема для создания распарсенного источника."""
    task_id: uuid.UUID


class ParsedSourceResponse(ParsedSourceBase):
    """Схема для ответа с данными распарсенного источника."""
    source_id: uuid.UUID
    task_id: uuid.UUID
    is_processed: bool
    processed_at: Optional[datetime] = None
    created_source_id: Optional[uuid.UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ExtractMetadataRequest(BaseModel):
    """Запрос на извлечение метаданных из URL."""
    url: AnyUrl


class ExtractMetadataResponse(BaseModel):
    """Ответ с извлеченными метаданными из URL."""
    url: AnyUrl
    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[AnyUrl] = None
    content_type: Optional[str] = None
    publication_date: Optional[datetime] = None
    author: Optional[str] = None
    source_site: Optional[str] = None
    language: Optional[str] = None
    keywords: Optional[List[str]] = None
    content: Optional[str] = None
"""
Модели данных для таблицы задач парсинга.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.content.parser_service.database import Base


class TaskStatus(str, Enum):
    """Статусы задач парсинга."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskType(str, Enum):
    """Типы задач парсинга."""
    SINGLE_URL = "single_url"
    WEBSITE = "website"
    RSS = "rss"
    SCHEDULED = "scheduled"


class ParserTask(Base):
    """
    Модель для задачи парсинга источников.
    """
    __tablename__ = "parser_tasks"

    # Основные поля
    task_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(2048), nullable=False)

    # Параметры задачи
    task_type = Column(String, nullable=False, default=TaskType.SINGLE_URL.value)
    status = Column(String, nullable=False, default=TaskStatus.PENDING.value)
    params = Column(JSON, nullable=True)  # Дополнительные параметры для парсинга

    # Связи
    created_by = Column(UUID(as_uuid=True), nullable=True)

    # Метаданные задачи
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

    # Результаты
    sources_found = Column(Integer, default=0)
    sources_created = Column(Integer, default=0)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<ParserTask {self.title} ({self.status})>"


class ScheduledParserTask(Base):
    """
    Модель для периодически запускаемых задач парсинга.
    """
    __tablename__ = "scheduled_parser_tasks"

    scheduled_task_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("parser_tasks.task_id"), nullable=False)

    # Настройки расписания (в формате cron или интервал)
    schedule_type = Column(String(20), nullable=False)  # 'cron' или 'interval'
    schedule_value = Column(String(100), nullable=False)  # cron-выражение или интервал в секундах

    # Дополнительные настройки
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)

    # Связи
    task = relationship("ParserTask")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<ScheduledParserTask {self.schedule_type}:{self.schedule_value}>"


class ParsedSource(Base):
    """
    Промежуточная модель для хранения данных перед передачей в основной сервис контента.
    """
    __tablename__ = "parsed_sources"

    source_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("parser_tasks.task_id"), nullable=False)

    # Данные источника
    url = Column(String(2048), nullable=False, unique=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    thumbnail_url = Column(String(2048), nullable=True)
    content_type = Column(String(50), nullable=True)
    publication_date = Column(DateTime, nullable=True)

    # Мета-информация
    author = Column(String(255), nullable=True)
    source_site = Column(String(255), nullable=True)
    language = Column(String(10), nullable=True)
    keywords = Column(JSON, nullable=True)  # массив ключевых слов

    # Статус обработки
    is_processed = Column(Boolean, default=False)
    processed_at = Column(DateTime, nullable=True)
    created_source_id = Column(UUID(as_uuid=True), nullable=True)  # ID источника в основном сервисе

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    task = relationship("ParserTask")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<ParsedSource {self.title}>"

"""
Схемы Pydantic для валидации данных жалоб и модерации.
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ComplaintStatus(str, Enum):
    """Статусы жалоб."""
    PENDING = "pending"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class ComplaintReason(str, Enum):
    """Причины жалоб."""
    SPAM = "spam"
    MISLEADING = "misleading"
    INAPPROPRIATE = "inappropriate"
    COPYRIGHT = "copyright"
    OTHER = "other"


class ComplaintBase(BaseModel):
    """Базовая схема для жалобы."""
    source_id: uuid.UUID
    reason: ComplaintReason
    description: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    """Схема для создания жалобы."""
    user_id: uuid.UUID


class ComplaintUpdate(BaseModel):
    """Схема для обновления статуса жалобы."""
    status: ComplaintStatus
    resolved_date: Optional[datetime] = None


class Complaint(ComplaintBase):
    """Схема для полного представления жалобы."""
    complaint_id: uuid.UUID
    user_id: uuid.UUID
    status: ComplaintStatus
    created_date: datetime
    resolved_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComplaintWithDetails(Complaint):
    """Схема для представления жалобы с дополнительными деталями."""
    user_name: Optional[str] = None
    source_title: Optional[str] = None
    source_url: Optional[str] = None

    class Config:
        from_attributes = True

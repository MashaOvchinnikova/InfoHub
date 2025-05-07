"""
Модели данных для жалоб и модерации.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from src.moderation.admin_service.database import Base


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


class Complaint(Base):
    """
    Модель для жалоб пользователей.
    """
    __tablename__ = "complaint"

    complaint_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    source_id = Column(UUID(as_uuid=True), nullable=False)
    reason = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default=ComplaintStatus.PENDING)
    created_date = Column(DateTime, default=datetime.utcnow)
    resolved_date = Column(DateTime, nullable=True)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Complaint {self.complaint_id} by {self.user_id}>"

"""
Модели данных для таблицы пользователей в сервисе аутентификации.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.user.auth_service.database import Base


class UserAuth(Base):
    """
    Модель пользователя для аутентификации и авторизации.
    """
    __tablename__ = "user_auth"

    # Основные поля
    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # Статус аккаунта
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)

    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_date = Column(DateTime, nullable=True)

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<UserAuth {self.email}>"
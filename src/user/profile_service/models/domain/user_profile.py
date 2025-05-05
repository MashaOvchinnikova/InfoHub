"""
Модели данных для профилей пользователей.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.user.profile_service.database import Base


class UserProfile(Base):
    """
    Модель профиля пользователя с расширенной информацией.
    """
    __tablename__ = "user_profile"
    __table_args__ = {"schema": "profile_service_schema"}

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    bio = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    reputation_score = Column(Integer, default=0)

    # Связи с другими таблицами
    interests = relationship("UserInterest", back_populates="user")
    activities = relationship("Activity", back_populates="user")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<UserProfile {self.user_id}>"


class Interest(Base):
    """
    Модель для представления интересов/категорий.
    """
    __tablename__ = "interest"
    __table_args__ = {"schema": "profile_service_schema"}

    interest_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("profile_service_schema.interest.interest_id"), nullable=True)

    # Связи для иерархической структуры
    children = relationship("Interest",
                            remote_side=[interest_id],
                            backref=("parent"),
                            cascade="all, delete-orphan", single_parent=True)
    user_interests = relationship("UserInterest", back_populates="interest")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Interest {self.name}>"


class UserInterest(Base):
    """
    Связующая модель между пользователями и их интересами.
    """
    __tablename__ = "user_interest"
    __table_args__ = {"schema": "profile_service_schema"}

    user_interest_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profile_service_schema.user_profile.user_id"), nullable=False)
    interest_id = Column(UUID(as_uuid=True), ForeignKey("profile_service_schema.interest.interest_id"), nullable=False)
    weight = Column(Float, default=1.0)  # Вес интереса для пользователя

    # Связи
    user = relationship("UserProfile", back_populates="interests")
    interest = relationship("Interest", back_populates="user_interests")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<UserInterest {self.user_id}:{self.interest_id}>"


class Activity(Base):
    """
    Модель для отслеживания активности пользователей.
    """
    __tablename__ = "activity"
    __table_args__ = {"schema": "profile_service_schema"}

    activity_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profile_service_schema.user_profile.user_id"), nullable=False)
    activity_type = Column(String, nullable=False)  # view, add, comment, rate, etc.
    entity_type = Column(String, nullable=False)  # source, comment, collection, etc.
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    # Связи
    user = relationship("UserProfile", back_populates="activities")

    def __repr__(self):
        """Строковое представление объекта."""
        return f"<Activity {self.activity_type} by {self.user_id}>"

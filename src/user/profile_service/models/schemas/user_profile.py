"""
Схемы Pydantic для валидации данных профилей пользователей.
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class InterestBase(BaseModel):
    """Базовая схема для интереса."""
    name: str
    description: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None


class InterestCreate(InterestBase):
    """Схема для создания интереса."""
    pass


class InterestUpdate(BaseModel):
    """Схема для обновления интереса."""
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None


class Interest(InterestBase):
    """Схема для полного представления интереса."""
    interest_id: uuid.UUID

    class Config:
        from_attributes = True


class InterestHierarchy(Interest):
    """Схема для представления иерархии интересов."""
    children: List["InterestHierarchy"] = []

    class Config:
        from_attributes = True


class UserInterestBase(BaseModel):
    """Базовая схема для связи пользователя и интереса."""
    interest_id: uuid.UUID
    weight: float = 1.0


class UserInterestCreate(UserInterestBase):
    """Схема для создания связи пользователя и интереса."""
    pass


class UserInterest(UserInterestBase):
    """Схема для полного представления связи пользователя и интереса."""
    user_interest_id: uuid.UUID
    user_id: uuid.UUID
    interest: Interest

    class Config:
        from_attributes = True


class UserProfileBase(BaseModel):
    """Базовая схема для профиля пользователя."""
    bio: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    """Схема для создания профиля пользователя."""
    user_id: uuid.UUID


class UserProfileUpdate(BaseModel):
    """Схема для обновления профиля пользователя."""
    bio: Optional[str] = None


class UserProfile(UserProfileBase):
    """Схема для полного представления профиля пользователя."""
    user_id: uuid.UUID
    registration_date: datetime
    reputation_score: int
    interests: List[UserInterest] = []

    class Config:
        from_attributes = True


class ActivityBase(BaseModel):
    """Базовая схема для активности."""
    activity_type: str
    entity_type: str
    entity_id: uuid.UUID


class ActivityCreate(ActivityBase):
    """Схема для создания записи об активности."""
    user_id: uuid.UUID


class Activity(ActivityBase):
    """Схема для полного представления активности."""
    activity_id: uuid.UUID
    user_id: uuid.UUID
    created_date: datetime

    class Config:
        from_attributes = True

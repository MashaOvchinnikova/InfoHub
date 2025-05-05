"""
Схемы Pydantic для валидации данных при работе с пользователями.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, validator


class UserBase(BaseModel):
    """Базовая схема для пользователя."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Схема для создания пользователя."""
    password: str = Field(..., min_length=8)
    password_confirm: str = Field(...)

    @validator('password_confirm')
    def passwords_match(cls, v, values):
        """Проверка совпадения паролей."""
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v


class UserUpdate(BaseModel):
    """Схема для обновления данных пользователя."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_blocked: Optional[bool] = None


class UserInDB(UserBase):
    """Схема для представления пользователя из БД."""
    user_id: uuid.UUID
    is_active: bool
    is_admin: bool
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
    last_login_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Схема для ответа с данными пользователя."""
    user_id: uuid.UUID
    is_active: bool
    is_admin: bool
    is_blocked: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Схема для аутентификации пользователя."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Схема для токена доступа."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Схема для данных токена."""
    sub: str
    exp: int
    type: str


class RefreshToken(BaseModel):
    """Схема для обновления токена."""
    refresh_token: str


class ChangePassword(BaseModel):
    """Схема для смены пароля."""
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_new_password: str

    @validator('confirm_new_password')
    def passwords_match(cls, v, values):
        """Проверка совпадения паролей."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Новые пароли не совпадают')
        return v


class MessageResponse(BaseModel):
    """Схема для ответа с сообщением."""
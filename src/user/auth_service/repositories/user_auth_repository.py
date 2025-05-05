"""
Репозиторий для работы с пользователями в базе данных.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import Depends

from sqlalchemy.orm import Session
from src.user.auth_service.database import database
from src.user.auth_service.models.domain.user_auth import UserAuth
from src.user.auth_service.models.schemas.user_auth import UserCreate, UserUpdate
from src.user.auth_service.utils.password_handler import hash_password, verify_password


class UserAuthRepository:
    """
    Репозиторий для выполнения операций с пользователями в БД.
    """
    def __init__(self, db: Session = Depends(database.get_session)) -> None:
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> Optional[UserAuth]:
        """
        Получение пользователя по ID.

        Args:
            user_id: ID пользователя

        Returns:
            UserAuth | None: Объект пользователя или None, если не найден
        """
        return self.db.query(UserAuth).filter(UserAuth.user_id == user_id).first()

    def get_by_email(self, email: str) -> Optional[UserAuth]:
        """
        Получение пользователя по email.

        Args:
            email: Email пользователя

        Returns:
            UserAuth | None: Объект пользователя или None, если не найден
        """
        return self.db.query(UserAuth).filter(UserAuth.email == email).first()

    def get_by_username(self, username: str) -> Optional[UserAuth]:
        """
        Получение пользователя по имени пользователя.

        Args:
            username: Имя пользователя

        Returns:
            UserAuth | None: Объект пользователя или None, если не найден
        """
        return self.db.query(UserAuth).filter(UserAuth.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserAuth]:
        """
        Получение списка пользователей с пагинацией.

        Args:

            skip: Смещение для пагинации
            limit: Ограничение на количество записей

        Returns:
            List[UserAuth]: Список пользователей
        """
        return self.db.query(UserAuth).offset(skip).limit(limit).all()

    def create(self, user_data: UserCreate) -> UserAuth:
        """
        Создание нового пользователя.

        Args:
            user_data: Данные для создания пользователя

        Returns:
            UserAuth: Созданный пользователь
        """
        hashed_password = hash_password(user_data.password)
        db_user = UserAuth(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: uuid.UUID, user_data: UserUpdate) -> Optional[UserAuth]:
        """
        Обновление данных пользователя.

        Args:
            user_id: ID пользователя
            user_data: Данные для обновления

        Returns:
            UserAuth | None: Обновленный пользователь или None, если не найден
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        # Формирование словаря с данными для обновления
        update_data = user_data.dict(exclude_unset=True)

        # Обновление пользователя
        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self,user_id: uuid.UUID) -> bool:
        """
        Удаление пользователя.

        Args:
            user_id: ID пользователя

        Returns:
            bool: True если пользователь удален, False если не найден
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True

    def authenticate(self,email: str, password: str) -> Optional[UserAuth]:
        """
        Аутентификация пользователя.

        Args:
            email: Email пользователя
            password: Пароль пользователя

        Returns:
            UserAuth | None: Пользователь если аутентификация успешна, иначе None
        """
        db_user = self.get_by_email(email)
        if not db_user:
            return None
        if not verify_password(password, db_user.password_hash):
            return None

        # Обновление даты последнего входа
        db_user.last_login_date = datetime.utcnow()
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def change_password(self,user_id: uuid.UUID, new_password: str) -> bool:
        """
        Изменение пароля пользователя.

        Args:
            user_id: ID пользователя
            new_password: Новый пароль

        Returns:
            bool: True если пароль изменен, False если пользователь не найден
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False

        db_user.password_hash = hash_password(new_password)
        db_user.updated_at = datetime.utcnow()

        self.db.add(db_user)
        self.db.commit()
        return True
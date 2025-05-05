"""
Репозиторий для работы с профилями пользователей в базе данных.
"""
import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.moderation.admin_service.database import database
from src.user.profile_service.models.domain.user_profile import UserProfile
from src.user.profile_service.models.schemas.user_profile import UserProfileCreate, UserProfileUpdate

# Настройка логирования
logger = logging.getLogger(__name__)


class UserProfileRepository:
    """
    Репозиторий для выполнения операций с профилями пользователей в БД.
    """
    def __init__(self, db: Session = Depends(database.get_session)) -> None:
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> Optional[UserProfile]:
        """
        Получение профиля пользователя по ID.

        Args:
            user_id: ID пользователя

        Returns:
            UserProfile | None: Объект профиля пользователя или None, если не найден
        """
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def create(self, profile_data: UserProfileCreate) -> UserProfile:
        """
        Создание нового профиля пользователя.

        Args:
            profile_data: Данные для создания профиля

        Returns:
            UserProfile: Созданный профиль пользователя

        Raises:
            SQLAlchemyError: При ошибке создания профиля
        """
        try:
            db_profile = UserProfile(
                user_id=profile_data.user_id,
                bio=profile_data.bio
            )
            self.db.add(db_profile)
            self.db.commit()
            self.db.refresh(db_profile)
            logger.info(f"Создан профиль пользователя: {db_profile.user_id}")
            return db_profile
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при создании профиля пользователя: {e}")
            raise

    def update(self, user_id: uuid.UUID, profile_data: UserProfileUpdate) -> Optional[UserProfile]:
        """
        Обновление профиля пользователя.

        Args:
            user_id: ID профиля пользователя
            profile_data: Данные для обновления

        Returns:
            UserProfile | None: Обновленный профиль или None, если профиль не найден

        Raises:
            SQLAlchemyError: При ошибке обновления профиля
        """
        db_profile = self.get_by_id(user_id)
        if not db_profile:
            logger.warning(f"Попытка обновления несуществующего профиля: {user_id}")
            return None

        try:
            update_data = profile_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_profile, key, value)

            self.db.commit()
            self.db.refresh(db_profile)
            logger.info(f"Обновлен профиль пользователя: {user_id}")
            return db_profile
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при обновлении профиля пользователя: {e}")
            raise

    def delete(self, user_id: uuid.UUID) -> bool:
        """
        Удаление профиля пользователя.

        Args:
            user_id: ID профиля пользователя

        Returns:
            bool: True если профиль успешно удален, иначе False

        Raises:
            SQLAlchemyError: При ошибке удаления профиля
        """
        db_profile = self.get_by_id(user_id)
        if not db_profile:
            logger.warning(f"Попытка удаления несуществующего профиля: {user_id}")
            return False

        try:
            self.db.delete(db_profile)
            self.db.commit()
            logger.info(f"Удален профиль пользователя: {user_id}")
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при удалении профиля пользователя: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserProfile]:
        """
        Получение списка профилей пользователей с пагинацией.

        Args:
            skip: Количество профилей для пропуска
            limit: Максимальное количество профилей для возврата

        Returns:
            List[UserProfile]: Список профилей пользователей
        """
        return self.db.query(UserProfile).offset(skip).limit(limit).all()

    def update_reputation(self, user_id: uuid.UUID, points: int) -> Optional[UserProfile]:
        """
        Обновление репутации пользователя.

        Args:
            user_id: ID профиля пользователя
            points: Количество очков для добавления к репутации (может быть отрицательным)

        Returns:
            UserProfile | None: Обновленный профиль или None, если профиль не найден

        Raises:
            SQLAlchemyError: При ошибке обновления репутации
        """
        db_profile = self.get_by_id(user_id)
        if not db_profile:
            logger.warning(f"Попытка обновления репутации несуществующего профиля: {user_id}")
            return None

        try:
            db_profile.reputation_score += points
            self.db.commit()
            self.db.refresh(db_profile)
            logger.info(f"Обновлена репутация пользователя {user_id}: {points} очков")
            return db_profile
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Ошибка при обновлении репутации пользователя: {e}")
            raise
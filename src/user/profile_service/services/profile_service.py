"""
Сервисный слой для управления профилями пользователей.
"""
import logging
import uuid

from fastapi import Depends, HTTPException, status

from src.user.profile_service.repositories.profile_repository import UserProfileRepository
from src.user.profile_service.models.schemas.user_profile import (
    UserProfile, UserProfileCreate, UserProfileUpdate
)

# Настройка логирования
logger = logging.getLogger(__name__)


class ProfileService:
    """
    Сервис для управления профилями пользователей.
    """

    def __init__(self, profile_repo: UserProfileRepository = Depends(UserProfileRepository)):
        self.profile_repo = profile_repo

    async def create_profile(self, profile_data: UserProfileCreate) -> UserProfile:
        """
        Создание нового профиля пользователя.

        Args:
            profile_data: Данные для создания профиля

        Returns:
            UserProfile: Созданный профиль пользователя

        Raises:
            HTTPException: Если профиль с таким user_id уже существует
        """
        # Проверка, существует ли уже профиль для этого пользователя
        existing_profile =  self.profile_repo.get_by_id(profile_data.user_id)
        if existing_profile:
            logger.warning(f"Профиль для пользователя {profile_data.user_id} уже существует")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Профиль для этого пользователя уже существует"
            )

        try:
            # Создание профиля
            profile = self.profile_repo.create(profile_data)
            logger.info(f"Создан профиль для пользователя {profile.user_id}")
            return profile
        except Exception as e:
            logger.error(f"Ошибка при создании профиля: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при создании профиля пользователя"
            )

    async def get_profile(self, user_id: uuid.UUID) -> UserProfile:
        """
        Получение профиля пользователя по ID.

        Args:
            user_id: ID пользователя

        Returns:
            UserProfile: Профиль пользователя

        Raises:
            HTTPException: Если профиль не найден
        """
        profile = self.profile_repo.get_by_id(user_id)
        if not profile:
            logger.warning(f"Профиль для пользователя {user_id} не найден")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль пользователя не найден"
            )
        return profile

    async def update_profile(self, user_id: uuid.UUID, profile_data: UserProfileUpdate) -> UserProfile:
        """
        Обновление профиля пользователя.

        Args:
            user_id: ID пользователя
            profile_data: Данные для обновления профиля

        Returns:
            UserProfile: Обновленный профиль пользователя

        Raises:
            HTTPException: Если профиль не найден
        """
        # Проверка, существует ли профиль
        existing_profile = self.profile_repo.get_by_id(user_id)
        if not existing_profile:
            logger.warning(f"Профиль для пользователя {user_id} не найден при попытке обновления")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль пользователя не найден"
            )

        try:
            # Обновление профиля
            updated_profile = self.profile_repo.update(user_id, profile_data)
            logger.info(f"Обновлен профиль для пользователя {user_id}")
            return updated_profile
        except Exception as e:
            logger.error(f"Ошибка при обновлении профиля: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при обновлении профиля пользователя"
            )

    async def delete_profile(self, user_id: uuid.UUID) -> None:
        """
        Удаление профиля пользователя.

        Args:
            user_id: ID пользователя

        Raises:
            HTTPException: Если профиль не найден
        """
        # Проверка, существует ли профиль
        existing_profile = self.profile_repo.get_by_id(user_id)
        if not existing_profile:
            logger.warning(f"Профиль для пользователя {user_id} не найден при попытке удаления")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль пользователя не найден"
            )

        try:
            # Удаление профиля
            self.profile_repo.delete(user_id)
            logger.info(f"Удален профиль для пользователя {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при удалении профиля: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при удалении профиля пользователя"
            )

    async def update_reputation(self, user_id: uuid.UUID, score_change: int) -> UserProfile:
        """
        Обновление репутации пользователя.

        Args:
            user_id: ID пользователя
            score_change: Изменение репутации (положительное или отрицательное)

        Returns:
            UserProfile: Обновленный профиль пользователя

        Raises:
            HTTPException: Если профиль не найден
        """
        # Проверка, существует ли профиль
        existing_profile = self.profile_repo.get_by_id(user_id)
        if not existing_profile:
            logger.warning(f"Профиль для пользователя {user_id} не найден при попытке обновления репутации")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль пользователя не найден"
            )

        try:
            # Обновление репутации
            updated_profile = self.profile_repo.update_reputation(user_id, score_change)
            logger.info(f"Обновлена репутация для пользователя {user_id}, изменение: {score_change}")
            return updated_profile
        except Exception as e:
            logger.error(f"Ошибка при обновлении репутации: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ошибка при обновлении репутации пользователя"
            )
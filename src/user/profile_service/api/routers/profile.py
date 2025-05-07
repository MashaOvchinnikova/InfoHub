"""
Маршруты для работы с профилями пользователей.
"""
import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.user.profile_service.api.dependencies import authentication_required
from src.user.profile_service.models.schemas.user_profile import (
    UserProfile, UserProfileCreate, UserProfileUpdate, Activity, ActivityCreate
)
from src.user.profile_service.services.profile_service import ProfileService
from src.user.auth_service.models.schemas.user_auth import UserResponse

# Настройка логирования
logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post("", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def create_profile(
        profile_data: UserProfileCreate,
        profile_service: ProfileService = Depends(ProfileService),
        current_user: UserResponse = Depends(authentication_required)
):
    """
    Создание нового профиля пользователя.

    Args:
        profile_data: Данные для создания профиля
        profile_service: Сервис для работы с профилями
        current_user: Информация о текущем пользователе

    Returns:
        UserProfile: Созданный профиль пользователя

    Raises:
        HTTPException: Если пользователь пытается создать профиль для другого пользователя
    """
    # Проверка, что пользователь создает профиль для себя
    if str(profile_data.user_id) != str(current_user.user_id) and not current_user.is_admin:
        logger.warning(f"Пользователь {current_user.user_id} пытается создать профиль для {profile_data.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Можно создать профиль только для своего аккаунта"
        )

    return await profile_service.create_profile(profile_data)


@router.get("/{user_id}", response_model=UserProfile)
async def get_profile(
        user_id: uuid.UUID,
        profile_service: ProfileService = Depends(ProfileService),
        current_user: UserResponse = Depends(authentication_required)
):
    """
    Получение профиля пользователя по ID.

    Args:
        user_id: ID пользователя
        profile_service: Сервис для работы с профилями
        current_user: Информация о текущем пользователе

    Returns:
        UserProfile: Профиль пользователя
    """
    return await profile_service.get_profile(user_id)


@router.put("/{user_id}", response_model=UserProfile)
async def update_profile(
        user_id: uuid.UUID,
        profile_data: UserProfileUpdate,
        profile_service: ProfileService = Depends(ProfileService),
        current_user: UserResponse = Depends(authentication_required)
):
    """
    Обновление профиля пользователя.

    Args:
        user_id: ID пользователя
        profile_data: Данные для обновления профиля
        profile_service: Сервис для работы с профилями

    Returns:
        UserProfile: Обновленный профиль пользователя
    """
    return await profile_service.update_profile(user_id, profile_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
        user_id: uuid.UUID,
        profile_service: ProfileService = Depends(ProfileService),
        current_user: UserResponse = Depends(authentication_required)
):
    """
    Удаление профиля пользователя.

    Args:
        user_id: ID пользователя
        profile_service: Сервис для работы с профилями

    Returns:
        None
    """
    await profile_service.delete_profile(user_id)
    return None


# @router.post("/{user_id}/activities", response_model=Activity, status_code=status.HTTP_201_CREATED)
# async def create_activity(
#         user_id: uuid.UUID,
#         activity_data: ActivityCreate,
#         profile_service: ProfileService = Depends(ProfileService),
#         current_user: UserResponse = Depends(authentication_required)
# ):
#     """
#     Создание записи об активности пользователя.
#
#     Args:
#         user_id: ID пользователя
#         activity_data: Данные об активности
#         profile_service: Сервис для работы с профилями
#
#     Returns:
#         Activity: Созданная запись об активности
#     """
#     # Проверка, что user_id в запросе совпадает с user_id в данных активности
#     if user_id != activity_data.user_id:
#         logger.warning("Несоответствие ID пользователя в запросе и данных активности")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="ID пользователя в запросе и данных активности должны совпадать"
#         )
#
#     return await profile_service.create_activity(activity_data)
#
#
# @router.get("/{user_id}/activities", response_model=List[Activity])
# async def get_user_activities(
#         user_id: uuid.UUID,
#         skip: int = 0,
#         limit: int = 100,
#         activity_type: str = None,
#         entity_type: str = None,
#         profile_service: ProfileService = Depends(ProfileService),
#         _: bool = Depends(lambda user_id=user_id, current_user=Depends(get_current_user):
#                           validate_user_access(user_id, current_user))
# ):
#     """
#     Получение списка активностей пользователя с фильтрацией.
#
#     Args:
#         user_id: ID пользователя
#         skip: Количество записей для пропуска (для пагинации)
#         limit: Максимальное количество возвращаемых записей
#         activity_type: Тип активности для фильтрации
#         entity_type: Тип сущности для фильтрации
#         profile_service: Сервис для работы с профилями
#
#     Returns:
#         List[Activity]: Список активностей пользователя
#     """
#     return await profile_service.get_user_activities(
#         user_id,
#         skip=skip,
#         limit=limit,
#         activity_type=activity_type,
#         entity_type=entity_type
#     )
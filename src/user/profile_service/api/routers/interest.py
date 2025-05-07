"""
Маршруты для работы с интересами.
"""
import uuid
import logging
from typing import List

from fastapi import APIRouter, Depends, Query, status

from src.user.profile_service.api.dependencies import authentication_required, admin_required
from src.user.profile_service.models.schemas.user_profile import (
    Interest, InterestCreate, InterestUpdate, InterestHierarchy
)
from src.user.auth_service.models.schemas.user_auth import UserResponse

# from src.user.profile_service.services.interest_service import InterestService

# Настройка логирования
logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter(prefix="/interests", tags=["interests"])


@router.get("", response_model=List[Interest])
async def get_interests(
        name: str = None,
        parent_id: uuid.UUID = None,
        skip: int = 0,
        limit: int = 100,
        current_user: UserResponse = Depends(authentication_required)
        # interest_service: InterestService = Depends(InterestService),
        # _: dict = Depends(get_current_user)
):
    """
    Получение списка интересов с возможностью фильтрации.

    Args:
        name: Фильтр по названию интереса
        parent_id: Фильтр по ID родительского интереса
        skip: Количество записей для пропуска (для пагинации)
        limit: Максимальное количество возвращаемых записей
        interest_service: Сервис для работы с интересами

    Returns:
        List[Interest]: Список интересов, соответствующих критериям фильтрации
    """
    # return await interest_service.get_interests(
    #     name=name,
    #     parent_id=parent_id,
    #     skip=skip,
    #     limit=limit
    # )
    pass


@router.get("/hierarchy", response_model=List[InterestHierarchy])
async def get_interest_hierarchy(
        root_only: bool = Query(False, description="Вернуть только корневые категории"),
        current_user: UserResponse = Depends(authentication_required),
        # interest_service: InterestService = Depends(InterestService),
        # _: dict = Depends(get_current_user)
):
    """
    Получение иерархической структуры интересов.

    Args:
        root_only: Вернуть только корневые категории
        interest_service: Сервис для работы с интересами

    Returns:
        List[InterestHierarchy]: Иерархическая структура интересов
    """
    # return await interest_service.get_interest_hierarchy(root_only=root_only)
    pass


@router.get("/{interest_id}", response_model=Interest)
async def get_interest(
        interest_id: uuid.UUID,
        current_user: UserResponse = Depends(authentication_required)
        # interest_service: InterestService = Depends(InterestService),
        # _: dict = Depends(get_current_user)
):
    """
    Получение информации об интересе по ID.

    Args:
        interest_id: ID интереса
        interest_service: Сервис для работы с интересами

    Returns:
        Interest: Информация об интересе
    """
    # return await interest_service.get_interest(interest_id)
    pass


@router.post("", response_model=Interest, status_code=status.HTTP_201_CREATED)
async def create_interest(
        interest_data: InterestCreate,
        current_user: UserResponse = Depends(authentication_required)
        # interest_service: InterestService = Depends(InterestService),
        # _: bool = Depends(admin_required)
):
    """
    Создание нового интереса (только для администраторов).

    Args:
        interest_data: Данные для создания интереса
        interest_service: Сервис для работы с интересами

    Returns:
        Interest: Созданный интерес
    """
    # return await interest_service.create_interest(interest_data)
    pass


@router.put("/{interest_id}", response_model=Interest)
async def update_interest(
        interest_id: uuid.UUID,
        interest_data: InterestUpdate,
        current_user: UserResponse = Depends(authentication_required)
        # interest_service: InterestService = Depends(InterestService),
        # _: bool = Depends(admin_required)
):
    """
    Обновление интереса (только для администраторов).

    Args:
        interest_id: ID интереса
        interest_data: Данные для обновления интереса
        interest_service: Сервис для работы с интересами

    Returns:
        Interest: Обновленный интерес
    """
    # return await interest_service.update_interest(interest_id, interest_data)
    pass


@router.delete("/{interest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interest(
        interest_id: uuid.UUID,
        current_user: UserResponse = Depends(authentication_required)
        # interest_service: InterestService = Depends(InterestService),
        # _: bool = Depends(admin_required)
):
    """
    Удаление интереса (только для администраторов).

    Args:
        interest_id: ID интереса
        interest_service: Сервис для работы с интересами

    Returns:
        None
    """
    # await interest_service.delete_interest(interest_id)
    # return None
    pass


@router.get("/{interest_id}/related", response_model=List[Interest])
async def get_related_interests(
        interest_id: uuid.UUID,
        limit: int = 10,
        current_user: UserResponse = Depends(authentication_required)

        # interest_service: InterestService = Depends(InterestService),
        # _: dict = Depends(get_current_user)
):
    """
    Получение интересов, связанных с заданным интересом.

    Args:
        interest_id: ID интереса
        limit: Максимальное количество возвращаемых связанных интересов
        interest_service: Сервис для работы с интересами

    Returns:
        List[Interest]: Список связанных интересов
    """
    # return await interest_service.get_related_interests(interest_id, limit=limit)
    pass
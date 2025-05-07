"""
Маршруты для управления активностями пользователей.
"""
import uuid
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status

# from src.user.profile_service.api.dependencies import get_current_user_id
from src.user.profile_service.models.schemas.user_profile import Activity, ActivityCreate
# from src.user.profile_service.services.activity_service import ActivityService

# Настройка логирования
logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=Activity, status_code=status.HTTP_201_CREATED)
async def record_activity(
        activity_data: ActivityCreate,
        # current_user_id: uuid.UUID = Depends(get_current_user_id),
        # activity_service: ActivityService = Depends(ActivityService)
) -> Activity:
    """
    Запись новой активности пользователя.

    Args:
        activity_data: Данные об активности
        current_user_id: ID текущего пользователя
        activity_service: Сервис для работы с активностями

    Returns:
        Activity: Записанная активность
    """
    # # Проверка, что текущий пользователь совпадает с пользователем активности
    # if current_user_id != activity_data.user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Нельзя записывать активность от имени другого пользователя"
    #     )
    #
    # return activity_service.create(activity_data)
    pass


@router.get("/me", response_model=List[Activity])
async def get_my_activities(
        activity_type: Optional[str] = Query(None, description="Фильтр по типу активности"),
        entity_type: Optional[str] = Query(None, description="Фильтр по типу сущности"),
        from_date: Optional[datetime] = Query(None, description="Начальная дата для фильтрации"),
        to_date: Optional[datetime] = Query(None, description="Конечная дата для фильтрации"),
        limit: int = Query(10, ge=1, le=100, description="Количество записей на странице"),
        offset: int = Query(0, ge=0, description="Смещение для пагинации"),
        # current_user_id: uuid.UUID = Depends(get_current_user_id),
        # activity_service: ActivityService = Depends(ActivityService)
) -> List[Activity]:
    """
    Получение активностей текущего пользователя с возможностью фильтрации.

    Args:
        activity_type: Опциональный фильтр по типу активности
        entity_type: Опциональный фильтр по типу сущности
        from_date: Опциональный фильтр по начальной дате
        to_date: Опциональный фильтр по конечной дате
        limit: Количество записей на странице
        offset: Смещение для пагинации
        current_user_id: ID текущего пользователя
        activity_service: Сервис для работы с активностями

    Returns:
        List[Activity]: Список активностей пользователя
    """
    # return activity_service.get_by_user_id(
    #     user_id=current_user_id,
    #     activity_type=activity_type,
    #     entity_type=entity_type,
    #     from_date=from_date,
    #     to_date=to_date,
    #     limit=limit,
    #     offset=offset
    # )
    pass


@router.get("/{user_id}", response_model=List[Activity])
async def get_user_activities(
        user_id: uuid.UUID = Path(..., description="ID пользователя"),
        activity_type: Optional[str] = Query(None, description="Фильтр по типу активности"),
        entity_type: Optional[str] = Query(None, description="Фильтр по типу сущности"),
        from_date: Optional[datetime] = Query(None, description="Начальная дата для фильтрации"),
        to_date: Optional[datetime] = Query(None, description="Конечная дата для фильтрации"),
        limit: int = Query(10, ge=1, le=100, description="Количество записей на странице"),
        offset: int = Query(0, ge=0, description="Смещение для пагинации"),
        # current_user_id: uuid.UUID = Depends(get_current_user_id),
        # activity_service: ActivityService = Depends(ActivityService)
) -> List[Activity]:
    """
    Получение активностей указанного пользователя (публичные данные).

    Args:
        user_id: ID пользователя, активности которого запрашиваются
        activity_type: Опциональный фильтр по типу активности
        entity_type: Опциональный фильтр по типу сущности
        from_date: Опциональный фильтр по начальной дате
        to_date: Опциональный фильтр по конечной дате
        limit: Количество записей на странице
        offset: Смещение для пагинации
        current_user_id: ID текущего пользователя (для проверки прав доступа)
        activity_service: Сервис для работы с активностями

    Returns:
        List[Activity]: Список активностей пользователя

    Raises:
        HTTPException: Если у текущего пользователя нет прав для просмотра активностей
    """
    # Проверка прав доступа - пользователь может видеть только свои активности или публичные
    # В данной реализации для простоты все активности считаются публичными

    # return activity_service.get_by_user_id(
    #     user_id=user_id,
    #     activity_type=activity_type,
    #     entity_type=entity_type,
    #     from_date=from_date,
    #     to_date=to_date,
    #     limit=limit,
    #     offset=offset
    # )
    pass


@router.get("/{user_id}/{activity_id}", response_model=Activity)
async def get_activity_by_id(
        user_id: uuid.UUID = Path(..., description="ID пользователя"),
        activity_id: uuid.UUID = Path(..., description="ID активности"),
        # current_user_id: uuid.UUID = Depends(get_current_user_id),
        # activity_service: ActivityService = Depends(ActivityService)
) -> Activity:
    """
    Получение конкретной активности пользователя по ID.

    Args:
        user_id: ID пользователя
        activity_id: ID активности
        current_user_id: ID текущего пользователя (для проверки прав доступа)
        activity_service: Сервис для работы с активностями

    Returns:
        Activity: Данные активности

    Raises:
        HTTPException: Если активность не найдена или нет прав доступа
    """
    # activity = activity_service.get_by_id(activity_id)
    #
    # if not activity:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Активность с ID {activity_id} не найдена"
    #     )
    #
    # if activity.user_id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Активность с ID {activity_id} не принадлежит пользователю с ID {user_id}"
    #     )
    #
    # # Проверка прав доступа - пользователь может видеть только свои активности или публичные
    # # В данной реализации для простоты все активности считаются публичными
    #
    # return activity
    pass
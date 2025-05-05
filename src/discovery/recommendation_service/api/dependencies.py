"""
Зависимости для API-эндпоинтов.
"""
import logging

import httpx
from typing import Dict, Any, Optional
from fastapi import Depends, HTTPException, status, Header

from src.discovery.recommendation_service.config import settings
from src.user.auth_service.models.schemas.user_auth import UserResponse
from src.user.auth_service.services.current_user import get_current_user as get_user
# Настройка логирования
logger = logging.getLogger(__name__)


# # get_current_user для тестирования
# async def get_current_user(user: UserResponse = Depends(get_user)) -> UserResponse:
#     return user

async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> UserResponse:
    """
    Получение информации о текущем пользователе через сервис аутентификации.

    Args:
        authorization: JWT-токен из заголовка запроса

    Returns:
        Dict[str, Any]: Информация о пользователе

    Raises:
        HTTPException: Если токен отсутствует, недействителен или пользователь не найден
    """
    if not authorization:
        logger.warning("Отсутствует токен авторизации в заголовке запроса")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется аутентификация",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization
    if authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]

    # Выполнение запроса к сервису аутентификации для проверки токена
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/api/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            if response.status_code != 200:
                logger.warning(f"Ошибка при проверке токена: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Недействительный токен аутентификации",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_data = response.json()
            return UserResponse.model_validate(user_data)
    except httpx.RequestError as e:
        logger.error(f"Ошибка при обращении к сервису аутентификации: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис аутентификации недоступен",
        )


async def authentication_required(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
      Проверка наличия аутентификации у пользователя.

      Args:
          current_user: Информация о текущем пользователе

      Returns:
          UserResponse: Информация о текущем пользователе

      Raises:
          HTTPException: Если пользователь не аутентифицирован
      """
    return current_user


async def admin_required(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Проверка наличия прав администратора у пользователя.

    Args:
        current_user: Информация о текущем пользователе

    Returns:
        bool: True, если пользователь имеет права администратора

    Raises:
        HTTPException: Если пользователь не является администратором
    """
    if current_user.is_admin:
        return current_user

    logger.warning(f"Попытка выполнения административной операции пользователем {current_user.user_id}")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Требуются права администратора"
    )

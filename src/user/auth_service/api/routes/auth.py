"""
Маршруты для аутентификации и авторизации пользователей.
"""
import logging
from typing import Any

from fastapi import APIRouter, Depends, status

from src.user.auth_service.api.dependencies import get_current_user
from src.user.auth_service.models.schemas.user_auth import (Token, UserLogin, UserCreate, UserResponse,
                                                            MessageResponse, RefreshToken, ChangePassword)
from src.user.auth_service.models.domain.user_auth import UserAuth
from src.user.auth_service.services.auth_service import AuthService

# Настройка логирования
logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserCreate,
        auth_service: AuthService = Depends(AuthService)
) -> Any:
    """
    Регистрация нового пользователя.

    Args:
        user_data: Данные для создания пользователя
        auth_service: Сервис авторизации
    Returns:
        UserResponse: Информация о созданном пользователе

    Raises:
        HTTPException: Если email или имя пользователя уже существуют
    """
    return auth_service.register_user(user_data)


@router.post("/login", response_model=Token)
async def login(
        login_data: UserLogin,
        auth_service: AuthService = Depends(AuthService)
) -> Any:
    """
    Аутентификация пользователя и получение токена доступа.

    Args:
        login_data: Данные для входа
        auth_service: Сервис авторизации

    Returns:
        Token: Токены доступа и обновления

    Raises:
        HTTPException: Если аутентификация не удалась
    """
    return auth_service.authenticate_user(login_data)

#
# @router.post("/oauth/token", response_model=Token)
# async def login_oauth(
#         login_data: UserLogin,
#         auth_service: AuthService = Depends(AuthService)
# ) -> Any:
#     """
#     Стандартный OAuth2 эндпоинт для аутентификации.
#
#     Args:
#         login_data: Данные для входа
#         auth_service: Сервис авторизации
#
#     Returns:
#         Token: Токены доступа и обновления
#
#     Raises:
#         HTTPException: Если аутентификация не удалась
#     """
#     auth_service.authenticate_user(login_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(
        refresh_token: RefreshToken,
        auth_service: AuthService = Depends(AuthService)
) -> Any:
    """
    Обновление токена доступа по refresh токену.

    Args:
        refresh_token: Refresh токен
        auth_service: Сервис авторизации

    Returns:
        Token: Новые токены доступа и обновления

    Raises:
        HTTPException: Если токен обновления недействителен
    """
    return auth_service.refresh_token(refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
        current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Получение информации о текущем пользователе.

    Args:
        current_user: Текущий аутентифицированный пользователь

    Returns:
        UserResponse: Информация о пользователе
    """
    return current_user


@router.post("/change_password", response_model=MessageResponse)
async def change_password(
        password_data: ChangePassword,
        current_user: UserResponse = Depends(get_current_user),
        auth_service: AuthService = Depends(AuthService)
) -> Any:
    """
    Изменение пароля текущего пользователя.

    Args:
        password_data: Данные для изменения пароля
        current_user: Текущий аутентифицированный пользователь
        auth_service: Сервис авторизации


    Returns:
        MessageResponse: Сообщение об успешном изменении пароля

    Raises:
        HTTPException: Если текущий пароль неверен
    """
    return auth_service.change_user_password(password_data, current_user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
        current_user: UserAuth = Depends(get_current_user)
) -> Any:
    """
    Выход пользователя из системы.

    На стороне сервера не требуется особых действий, так как используется JWT.
    В реальном приложении здесь можно реализовать черный список токенов.

    Args:
        current_user: Текущий аутентифицированный пользователь

    Returns:
        MessageResponse: Сообщение об успешном выходе
    """
    logger.info(f"Пользователь вышел из системы: {current_user.email}")
    return {"message": "Выход выполнен успешно"}